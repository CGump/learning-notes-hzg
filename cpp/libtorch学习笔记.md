# libtorch学习笔记

记录libtorch开发的一些学习心得，顺带也补充了下opencv、C++的知识。

## 1、基于libtorch的yolov5模型部署

### 1.1 前处理

前处理这块主要是将输出的图像矩阵，转换为模型所要求输入的格式。主要由几个步骤：1、按比例缩放图像；2、填充白边；3、转RGB格式（因为是opencv读入）；4、像素值归一化；5、BHWC转为BCHW；6、如果是CUDA则要将数据折半。

#### 1.1.1 按比例缩放与填充

由于网络输入要求是800×800的图像，所以需要将原始的4096×3000的图像按照长边的比例缩放至800，这样一来短边就不足800像素，因此上下的空白区域要填补成灰色。因为灰色与背景相近，不容易产生明确的过渡断层。

```cpp
std::vector<float> pad_info = LetterboxImage(img_input, img_input, yolo_head_wh_);
```

这里的float列表pad_info包含左右空白区域的宽度，上下空白区域的宽度，是除过2的值，以及缩放的尺寸。在坐标反推时可以用到。

填充白边的操作也在`LetterboxImage`函数中实现，调用`cv::copyMakeBorder`函数

#### 1.1.2 转RGB和像素值归一化

这里都是调用opencv中的函数进行，没有多少问题

```cpp
cv::cvtColor(img_input, img_input, cv::COLOR_GRAY2RGB);  // BGR -> RGB
img_input.convertTo(img_input, CV_32FC3, 1.0f / 255.0f);  // 归一化 1/255
```

#### 1.1.3 维度转换

输入的维度顺序是batch、channel、h、w，因此要将opencv读入的3维度图像扩维并转成要求的维度顺序。libtorch提供了`torch::from_blob`的方法可以便捷地从各种数组数据转成Tensor，并操作它的维度形式。同时，`tensor.permute`方法可以按照原tensor的维度顺序索引进行任意维度的变换。并使用`tensor.contiguous`方法使得切换后的数据在内存中是连续的，这样才能在后面计算时使用，具体关于contiguous方法的原理点击[这里](https://zhuanlan.zhihu.com/p/64551412)。

```cpp
torch::Tensor tensor_img = torch::from_blob(img_input.data, { 1, img_input.rows, img_input.cols, img_input.channels() }).to(device_);
tensor_img = tensor_img.permute({ 0, 3, 1, 2 }).contiguous();  // BHWC -> BCHW

```

#### 1.1.4 half型转换

如果是在CUDA上做推理，模型需要将数据类型转成half型（fp16，半精度浮点），通过以下进行判断：

```cpp
if (half_) {
    // 与模型输入的格式保持一致
    tensor_img = tensor_img.to(torch::kHalf);
}
```

### 1.2 推理阶段

推理阶段就没什么好说的，主要还是调用模型的`forward()`方法直接推理就可以，注意模型的输入和输出都是`torch::jit::IValue`的数据类型，需要提取出来转成tensor进行后处理。

```cpp
std::vector<torch::jit::IValue> inputs;
inputs.emplace_back(tensor_img);
torch::jit::IValue output = module_.forward(inputs);
torch::Tensor result = output.toTuple()->elements()[0].toTensor();
```

### 1.3 后处理

#### 1.3.1 置信度过滤

输出结果的结构是三个不同尺寸大小的输出和每种尺寸大小对应的三个锚框的检测结果，所有输出尺寸下每个方格都有一个预测信息。在800×800的输入下，三个输出结果的尺寸分别为100×100、50×50、25×25，因此在三个锚框下一共有100×100×3+50×50×3+25×25×3=39375个方格的预测结果下。每个预测结果中，包含4个坐标值、1个有无物体的预测、n个类别预测，一共是4+1+n个值。

因此在输出结果中，它的维度尺寸是n×39375×(5+n)。在单batch上的结果是`[1, 39375, 9]`.

这里通过一个掩膜的方法，按置信度阈值对result进行国立，从而通过`torch::masked_select`方法拿到每个大于预测置信度阈值的预测结果。

```cpp
int num_classes = result.size(2) - item_attr_size_; // num_classes = 4

torch::Tensor conf_mask = result.select(2, 4).ge(conf_thres_).unsqueeze(2);

torch::Tensor det = torch::masked_select(result[0], conf_mask[0]).view({ -1, num_classes + item_attr_size_ });
```

#### 1.3.2 类置信度

选取第1维度即为列，第5、6、7、8列的4个类别置信度与第4列中的有无物体置信度相乘最终得到了该类的置信度得分

```cpp
det.slice(1, item_attr_size_, item_attr_size_ + num_classes) *= det.select(1, 4).unsqueeze(1);
```

#### 1.3.3 中心点坐标转换

yolo输出的目标框格式是经典的中心点坐标+宽高的形式，因此需要转成角点进行后续的iou计算。这里就比较简单了，机械计算而已。

```cpp
torch::Tensor box_xywh = det.slice(1, 0, 4);
torch::Tensor box_xyxy = torch::zeros_like(box_xywh);
box_xyxy.select(1, 0) = box_xywh.select(1, 0) - box_xywh.select(1, 2).div(2); // x1
box_xyxy.select(1, 1) = box_xywh.select(1, 1) - box_xywh.select(1, 3).div(2); // y1
box_xyxy.select(1, 2) = box_xywh.select(1, 0) + box_xywh.select(1, 2).div(2); // x2
box_xyxy.select(1, 3) = box_xywh.select(1, 1) + box_xywh.select(1, 3).div(2); // y2
```

#### 1.3.4 类别索引值

坐标转换完后就是求出每个预选框的类别预测。之前已经做过了各个类别的置信度处理，这里就是选一个最高的就可以。5678四列的顺序是按照训练时类别名的顺序排列的，因此最高值所在的行索引，就对应着类别名列表的索引位置。

求完之后，与之前的`box_xyxy`合并，这就得到了n行6列的预测结果，每列分别是xyxy、置信度、类索引值。

```cpp
std::tuple<torch::Tensor, torch::Tensor> max_classes = torch::max(det.slice(1, item_attr_size_, item_attr_size_ + num_classes), 1);  // 这里是按列，对每行进行求最大值，max函数第二个参数为维度
torch::Tensor max_conf_score = std::get<0>(max_classes);  // tuple中第一个tensor是置信度
torch::Tensor max_conf_index = std::get<1>(max_classes);  // tuple第二个tensor是置信度的相对索引位置，也就直接是类别索引
max_conf_score = max_conf_score.to(torch::kFloat);  //转浮点，扩维
max_conf_index = max_conf_index.to(torch::kFloat).unsqueeze(1);  //转浮点，扩维
// 坐标、置信度、类别索引拼接在一起，n×6的二维张量，n为n个预测结果
det = torch::cat({ box_xyxy.slice(1, 0, 4), max_conf_score.unsqueeze(1), max_conf_index }, 1);
```

#### 1.3.4 NMS算法

接下来就是NMS算法，见第二章的详细叙述。

#### 1.3.5 坐标还原

这里不用多说，原来什么尺寸缩放的，目标框的坐标值就按什么尺寸反推回去就好了。还记得前处理的时候，已经计算出了缩放比例和宽度方向、高度方向的填充量（其中有一个必为0，不要问为什么）。直接计算后，将结果写入结构体输出即可。

```cpp
// 结构体定义
struct Detection {
    cv::Rect bbox;
    float score;
    int class_idx;
};
// 坐标还原函数
void Detector::ScaleCoordinates(std::vector<Detection>& data, float pad_w, float pad_h, float scale, const cv::Size& img_shape) {

    auto clip = [](float n, float lower, float upper) {
        return std::max(lower, std::min(n, upper));
    };

    std::vector<Detection> detections;
    for (auto& i : data) {
        float x1 = (i.bbox.tl().x - pad_w) / scale;  // x padding
        float y1 = (i.bbox.tl().y - pad_h) / scale;  // y padding
        float x2 = (i.bbox.br().x - pad_w) / scale;  // x padding
        float y2 = (i.bbox.br().y - pad_h) / scale;  // y padding

        x1 = clip(x1, 0, img_shape.width);
        y1 = clip(y1, 0, img_shape.height);
        x2 = clip(x2, 0, img_shape.width);
        y2 = clip(y2, 0, img_shape.height);

        i.bbox = cv::Rect(cv::Point(x1, y1), cv::Point(x2, y2));
    }
}
```

## 2、libtorch中实现NMS算法

通过转换后，`det`变量内部存放了4列角点坐标，1列置信度得分和1列类别预测索引

具体操作为：置信度排序→得到排序后的索引值→取第i个box→分别比较第i+1后所有box→计算IOU→删除大于IOU阈值的预测框索引值→输出第i个box的索引值

### 2.1 类别区分

在进行NMS算法前，使用了一个非常巧妙的办法使得各个类别的预测框可以区分开来：通过设定一个较大的坐标系数，并按照类别索引的序号进行相乘，累加至原来的坐标上，这样就将各个类别的检测框全部归类在不同的位置上。由于在进行NMS时，我们只需要拿到最终保留框的索引值，因此这样叠加并不会影响最终的检测框位置。实现逻辑如下：

```cpp
constexpr int max_wh = 4096;
torch::Tensor c = det.slice(1, item_attr_size_, item_attr_size_ + 1) * max_wh;
torch::Tensor offset_box = det.slice(1, 0, 4) + c;
```

### 2.2 置信度排序

由于NMS算法的特性，同一区域下保留置信度最高的，因此对于重叠度大于IOU阈值的检测框一定是删掉置信度低的值，所以排序后可以按照序号索引，对叠加的目标框进行过滤，当遇到删除时将索引序号置为-1，从而跳过大部分的检索情况，减少计算的效率。实现逻辑如下：

```cpp
// 排序后的tensor包装成了一个tuple，第1个是置信度，第2个是置信度所在原数组的索引位置
std::tuple<torch::Tensor, torch::Tensor> det_sorted = max_conf_score.sort(0, true);
// 直接通过std::get()方法拿到tuple第2个位置的置信度索引值
torch::Tensor conf_sorted_index = std::get<1>(det_sorted);
```

### 2.3 创建Accessor对象快速访问tensor

libtorch提供了accessor方法可以将Tensor转换为容易访问的accessor对象进行直接索引，更加快速和方便。由于还没有研究清楚CUDA下的accessor使用方法，所以这里做了CPU的转换。实测下，CPU直接做accessor访问要比CUDA下直接访问Tensor内元素更快且更稳定。这里注意数据类型，排序后的置信度索引是long型，如果直接用的化必须保证数据类型对于，这里为了更加明确，在CUDA上做了类型转换。

```cpp
auto offset_box_cpu = offset_box.cpu();  // 将Tensor拷贝到cpu
auto det_cpu = det.cpu();  // 将Tensor拷贝到cpu
auto conf_index = conf_sorted_index.to(torch::kInt).cpu();  // long型转int型，拷贝到cpu
const auto& det_cpu_array = det_cpu.accessor<float, 2>();  // 转化为accessor对象：<浮点型, 2维>
const auto& offset_boxes = offset_box_cpu.accessor<float, 2>();  // 转化为accessor对象：<浮点型, 2维>
const auto& conf_index_array = conf_index.accessor<int, 1>();  // 转化为accessor对象：<整型, 1维>
```

### 2.4 循环检索计算IOU

通过排序后的置信度索引列表，对原tensor进行索引，取出其中的box的左上角点、右下角点的坐标值并计算区域面积。IOU计算分别是当前box与后面所有的box进行比对，当IOU值大于设定的阈值时，由于前面的box置信度一定大于后面的box，所以将后面位置box的索引置为-1表示删除，从而进行区分，避免重复计算相同的box。所以在取出box的坐标时还要判断是否序号是-1。~~同时这里也直接将索引的box数值直接输出至结果的结构体中。~~(box中的数值是加了偏移量的，不可以直接使用)

```cpp
int num_box = conf_index_array.size(0);  // num_box = 计算要处理的box个数
for (int i = 0; i < num_box - 1; i++) {
    int idi = conf_index_array[i];  // 拿出第1个box
    // 这里要对索引值进行判断，如果是-1就跳过直接做下一个
    if (idi == -1) {
        continue;
    }

    float b1_x1 = offset_boxes[idi][0];  // box1_left+top_x1
    float b1_y1 = offset_boxes[idi][1];  // box1_left+top_y1
    float b1_x2 = offset_boxes[idi][2];  // box1_right+bottem_x2
    float b1_y2 = offset_boxes[idi][3];  // box1_right+bottem_y2
    float b1_area = (b1_x2 - b1_x1 + 1) * (b1_y2 - b1_y1 + 1);  // box1面积

    for (int j = i + 1; j < num_box; j++) {
        int idj = conf_index_array[j];  // 拿出第2个box
        // 这里要对索引值进行判断，如果是-1就跳过直接做下一个
        if ( idj == -1) {
            continue;
        }

        float b2_x1 = offset_boxes[idj][0];  // box2_left+top_x1
        float b2_y1 = offset_boxes[idj][1];  // box2_left+top_y1
        float b2_x2 = offset_boxes[idj][2];  // box2_left+top_x2
        float b2_y2 = offset_boxes[idj][3];  // box2_left+top_y2
        float b2_area = (b2_x2 - b2_x1 + 1) * (b2_y2 - b2_y1 + 1);  // box2面积
        float inter_rect_x1 = std::max(b1_x1, b2_x1);  // 交集区域左上角点x
        float inter_rect_y1 = std::max(b1_y1, b2_y1);  // 交集区域左上角点y
        float inter_rect_x2 = std::min(b1_x2, b2_x2);  // 交集区域右下角点x
        float inter_rect_y2 = std::min(b1_y2, b2_y2);  // 交集区域右下角点y
        float inter_area = std::max(inter_rect_x2 - inter_rect_x1 + 1, float(0)) * std::max(inter_rect_y2 - inter_rect_y1 + 1, float(0));  // 交集区域面积

        float iou = inter_area / (b1_area + b2_area - inter_area);  // 计算IOU

        if (iou >= iou_thres_) {
            conf_index[j] = -1;  // 如果iou值大于阈值，则将第j个box的索引置为-1
        }
    }
    // 直接在循环里将第i个box的值提取输出到结构体里，免得重复循环计算
    Detection t;
    t.bbox = cv::Rect(cv::Point(det_cpu_array[idi][0], det_cpu_array[idi][1]),
                      cv::Point(det_cpu_array[idi][2], det_cpu_array[idi][3]));
    t.score = det_cpu_array[idi][4];
    t.class_idx = det_cpu_array[idi][5];
    det_rst.emplace_back(t);
}

```

