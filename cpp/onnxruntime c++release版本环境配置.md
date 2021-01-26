# onnxruntime c++release版本环境配置

下载完成的C/C++release版本包含两个文件夹，其中`include/`为头文件存放位置，`lib/`为动态库存放位置。需要将这两个库的文件夹地址写入环境变量，在当前用户的`.bashrc`中添加：

```bash
export C_INCLUDE_PATH="/root/hzg/onnx/onnxruntime-linux-x64-1.6.0/include:$C_INCLUDE_PATH"
export CPLUS_INCLUDE_PATH="/root/hzg/onnx/onnxruntime-linux-x64-1.6.0/include:$CPLUS_INCLUDE_PATH"
export LD_LIBRARY_PATH="/root/hzg/onnx/onnxruntime-linux-x64-1.6.0/lib:$LD_LIBRARY_PATH"
(具体路径为自己的库位置)
```

但是在添加lib后没有效果，所以将`libonnxruntime.so`和`libonnxruntime.so.1.6.0`两个文件拷贝至系统的lib库`usr\lib`

```bash
sudo cp libonnxruntime.so /usr/lib
sudo cp libonnxruntime.so.1.6.0 /usr/lib
```

后续测试看如何能够关联自己的文件夹

其实很简单，只需要将library添加至环境变量即可：

```bash
export LIBRARY_PATH="/root/hzg/onnx/onnxruntime-linux-x64-1.6.0/lib:$LIBRARY_PATH"
```



