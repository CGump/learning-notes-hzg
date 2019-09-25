import numpy as np
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.contrib.tensorboard.plugins import projector
print("check tensorflow version: ", tf.__version__)
# tensorflow 手写VGG16



def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def conv_layer(x, ksize, strideX, strideY, bias_shape, name, padding='SAME'):
    '''
    卷积层
    input:输入
    ksize：卷积核尺寸，[核高，核宽，通道数，个数]
    strideX，strideY：核的移动量
    bias_shape：偏置大小
    name：卷积层名字
    '''
    with tf.name_scope(name):
        with tf.name_scope('wights'):
            w = weight_variable(ksize)
        with tf.name_scope('bias'):
            b = bias_variable(bias_shape)
        with tf.name_scope('conv_cul'):
            conv = tf.nn.conv2d(x, w, strides=[1, strideX, strideY, 1],padding=padding)
        with tf.name_scope('relu'):
            out = tf.nn.relu(conv + b)
    return out

def max_pool_layer(x, ksize, strideX, strideY, name, padding='SAME'):
    with tf.name_scope(name):
        return tf.nn.max_pool(x, ksize, strides=[1, strideX, strideY, 1], padding=padding)

def fc_layer(fc_input, w_shape, b_shape, name):
    with tf.name_scope(name):
        with tf.name_scope('fc_wights'):
            w = weight_variable(w_shape)
        with tf.name_scope('fc_bais'):
            b = bias_variable(b_shape)
        with tf.name_scope('fc_out'):
            out = tf.nn.relu(tf.matmul(fc_input, w) + b)
    return out

def variable_summarie(var):
    with tf.name_scope('summaries'):  # 大命名空间，计算一系列的参数
        mean = tf.reduce_mean(var)  # 计算参数平均值
        tf.summary.scalar('mean', mean)  # 给计算的参数命名为平均值
        with tf.name_scope('stddev'):  # 小命名空间，计算标准差
            stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))  # 计算标准差
        tf.summary.scalar('stddev', stddev)  # 命名为标准差
        tf.summary.scalar('max', tf.reduce_max(var))  # 计算并命名为最大值
        tf.summary.scalar('min', tf.reduce_min(var))  # 计算并命名为最小值
        tf.summary.histogram('histogram', var)  # 统计直方图

def read_records(filename, resize_height, resize_width, type=None):
    '''
    解析record文件:源文件的图像数据是RGB,uint8,[0,255],一般作为训练数据时,需要归一化到[0,1]
    :param filename:
    :param resize_height:
    :param resize_width:
    :param type:选择图像数据的返回类型
         None:默认将uint8-[0,255]转为float32-[0,255]
         normalization:归一化float32-[0,1]
         centralization:归一化float32-[0,1],再减均值中心化
    :return:
    '''
    # 创建文件队列,不限读取的数量
    filename_queue = tf.train.string_input_producer([filename])
    reader = tf.TFRecordReader()
    # reader从文件队列中读入一个序列化的样本
    _, serialized_example = reader.read(filename_queue)
    # 解析符号化的样本
    features = tf.parse_single_example(
        serialized_example,
        features={
            'image_raw': tf.FixedLenFeature([], tf.string),
            'height': tf.FixedLenFeature([], tf.int64),
            'width': tf.FixedLenFeature([], tf.int64),
            'depth': tf.FixedLenFeature([], tf.int64),
            'label': tf.FixedLenFeature([], tf.int64)
        }
    )
    tf_image = tf.decode_raw(features['image_raw'], tf.uint8)  # 获得图像原始的数据

    tf_height = features['height']
    tf_width = features['width']
    tf_depth = features['depth']
    tf_label = tf.cast(features['label'], tf.int32)
    # PS:恢复原始图像数据,reshape的大小必须与保存之前的图像shape一致,否则出错
    # tf_image=tf.reshape(tf_image, [-1])    # 转换为行向量
    tf_image = tf.reshape(
        tf_image, [resize_height, resize_width, 3])  # 设置图像的维度

    # 恢复数据后,才可以对图像进行resize_images:输入uint->输出float32
    # tf_image=tf.image.resize_images(tf_image,[224, 224])

    # 存储的图像类型为uint8,tensorflow训练时数据必须是tf.float32
    if type is None:
        tf_image = tf.cast(tf_image, tf.float32)
    elif type == 'normalization':  # [1]若需要归一化请使用:
        # 仅当输入数据是uint8,才会归一化[0,255]
        # tf_image = tf.image.convert_image_dtype(tf_image, tf.float32)
        tf_image = tf.cast(tf_image, tf.float32) * (1. / 255.0)  # 归一化
    elif type == 'centralization':
        # 若需要归一化,且中心化,假设均值为0.5,请使用:
        tf_image = tf.cast(tf_image, tf.float32) * (1. / 255) - 0.5  # 中心化

    # 这里仅仅返回图像和标签
    # return tf_image, tf_height,tf_width,tf_depth,tf_label
    return tf_image, tf_label

def get_batch_images(images, labels, batch_size, labels_nums, one_hot=True, shuffle=False, num_threads=1):
    '''
    :param images:图像
    :param labels:标签
    :param batch_size:
    :param labels_nums:标签个数
    :param one_hot:是否将labels转为one_hot的形式
    :param shuffle:是否打乱顺序,一般train时shuffle=True,验证时shuffle=False
    :return:返回batch的images和labels
    '''
    min_after_dequeue = 200
    # 保证capacity必须大于min_after_dequeue参数值
    capacity = min_after_dequeue + 3 * batch_size
    if shuffle:
        images_batch, labels_batch = tf.train.shuffle_batch([images, labels],
                                                            batch_size=batch_size,
                                                            capacity=capacity,
                                                            min_after_dequeue=min_after_dequeue,
                                                            num_threads=num_threads)
    else:
        images_batch, labels_batch = tf.train.batch([images, labels],
                                                    batch_size=batch_size,
                                                    capacity=capacity,
                                                    num_threads=num_threads)
    if one_hot:
        labels_batch = tf.one_hot(labels_batch, labels_nums, 1, 0)
    return images_batch, labels_batch

def get_example_nums(tf_records_filenames):
    '''
    统计tf_records图像的个数(example)个数
    :param tf_records_filenames: tf_records文件路径
    :return:
    '''
    nums = 0
    for record in tf.python_io.tf_record_iterator(tf_records_filenames):
        nums += 1
    return nums


# 网络训练参数设置
batch_size = 1  # 每个批次大小
epoch = 3  # 循环训练次数
class_num = 11  # 类别数
train_tfrecords_path = 'data/train224.tfrecords'
val_tfrecords_path = 'data/val224.tfrecords'
save_path = 'logs/'

# 训练数据读取，图片以.tfrecords存储，编码方式为one-hot
train_nums = get_example_nums(train_tfrecords_path)
val_nums = get_example_nums(val_tfrecords_path)
print('train nums:%d, val nums:%d'%(train_nums, val_nums))
steps = epoch * (train_nums//batch_size)  # 总迭代次数

# 训练集图片和标签读取
train_images, train_labels = read_records(train_tfrecords_path, 
                                          resize_height=224,
                                          resize_width=224, 
                                          type='normalization')
train_images_batch, train_labels_batch = get_batch_images(train_images, train_labels,
                                                          batch_size=batch_size, 
                                                          labels_nums=class_num,
                                                          one_hot=True, shuffle=True) # 训练集乱序，shuffle控制

# 验证集图片和标签读取
val_images, val_labels = read_records(val_tfrecords_path, 
                                      resize_height=224, 
                                      resize_width=224, 
                                      type='normalization')
val_images_batch, val_labels_batch = get_batch_images(val_images, val_labels,
                                                      batch_size=batch_size, 
                                                      labels_nums=class_num,
                                                      one_hot=True, shuffle=False) # 测试集不用乱序

#输入参数 x_image:224*224*3, y_label:onehot编码，None匹配批量
with tf.name_scope('input_layer'):
    x_image = tf.placeholder(tf.float32, [None, 224, 224, 3])
    y_label = tf.placeholder(tf.float32, [None, class_num])  # 假设分n类

# 第一层:2*conv+1*pool
conv1_1 = conv_layer(x_image, [3, 3, 3, 64], 1, 1, [64], 'conv1-1')
conv1_2 = conv_layer(conv1_1, [3, 3, 64, 64], 1, 1, [64], 'conv1-2')
pool1 = max_pool_layer(conv1_2, [1, 2, 2, 1], 2, 2, 'pool1')
# 输出 112*112*64

# 第二层：2*conv+1*pool
conv2_1 = conv_layer(pool1, [3, 3, 64, 128], 1, 1, [128], 'conv2-1')
conv2_2 = conv_layer(conv2_1, [3, 3, 128, 128], 1, 1, [128], 'conv2-2')
pool2 = max_pool_layer(conv2_2, [1, 2, 2, 1], 2, 2, 'pool2')
# 输出 56*56*128

# 第三层：3*conv+1*pool
conv3_1 = conv_layer(pool2, [3, 3, 128, 256], 1, 1, [256], 'conv3-1')
conv3_2 = conv_layer(conv3_1, [3, 3, 256, 256], 1, 1, [256], 'conv3-2')
conv3_3 = conv_layer(conv3_2, [3, 3, 256, 256], 1, 1, [256], 'conv3-3')
pool3 = max_pool_layer(conv3_3, [1, 2, 2, 1], 2, 2, 'pool3')
# 输出 28*28*256

# 第四层：3*conv+1*pool
conv4_1 = conv_layer(pool3, [3, 3, 256, 512], 1, 1, [512], 'conv4-1')
conv4_2 = conv_layer(conv4_1, [3, 3, 512, 512], 1, 1, [512], 'conv4-2')
conv4_3 = conv_layer(conv4_2, [3, 3, 512, 512], 1, 1, [512], 'conv4-3')
pool4 = max_pool_layer(conv4_3, [1, 2, 2, 1], 2, 2, 'pool4')
# 输出 14*14*512

# 第五层：3*conv+1*pool
conv5_1 = conv_layer(pool4, [3, 3, 512, 512], 1, 1, [512], 'conv5-1')
conv5_2 = conv_layer(conv5_1, [3, 3, 512, 512], 1, 1, [512], 'conv5-2')
conv5_3 = conv_layer(conv5_2, [3, 3, 512, 512], 1, 1, [512], 'conv5-3')
pool5 = max_pool_layer(conv5_3, [1, 2, 2, 1], 2, 2, 'pool4')
# 输出 7*7*512

fc_input = tf.reshape(pool4, [-1, 7*7*512])
fc_1 = fc_layer(fc_input, [7*7*512, 4096], [4096], name='fc_1')
dropout1 = tf.nn.dropout(fc_1, keep_prob=0.7, name='dropout1')

fc_2 = fc_layer(dropout1, [4096, 4096], [4096], 'fc_2')
dropout2 = tf.nn.dropout(fc_2, keep_prob=0.7, name='dropout2')

fc_3 = fc_layer(dropout2, [4096, class_num], [class_num], 'fc_3')
fc_prec = tf.nn.sigmoid(fc_3)

# 定义loss使用交叉熵，和adam优化函数
with tf.name_scope('loss'):
    loss = tf.reduce_mean(
        tf.nn.softmax_cross_entropy_with_logits(labels=y_label, logits=fc_prec))
    tf.summary.scalar('loss', loss)
with tf.name_scope('train'):
    train_step = tf.train.AdamOptimizer(0.01).minimize(loss)

# 计算准确率

with tf.name_scope('accuracy'):
    vgg_prediction = tf.nn.softmax(fc_prec)
    correct = tf.equal(tf.argmax(vgg_prediction, 1), tf.argmax(y_label, 1))
    vgg_accuracy = tf.reduce_mean(tf.cast(correct, tf.float32)) # 每个批次，布尔数组转换成浮点数计算均值
    tf.summary.scalar('accuracy', vgg_accuracy)

merged = tf.summary.merge_all()
init = tf.global_variables_initializer()
saver = tf.train.Saver()
max_acc = 0 #存放最优的准确率，用以迭代保存模型

with tf.Session() as sess:
    sess.run(init) # 初始化所有变量
    writer = tf.summary.FileWriter('logs/', sess.graph)
    print("-----train started-----")
    for i in range(steps + 1):
        batch_input_images, batch_input_labels = sess.run([train_images_batch, train_labels_batch])
        summary, _, train_loss = sess.run([merged, train_step, loss], 
                                          feed_dict={x_image:batch_input_images, y_label:batch_input_labels})

        if i%epoch == 0:
            val_max_number = int(val_nums/batch_size)
            val_losses = []
            val_accs = []
            for _ in xrange(val_max_number):
                val_x, val_y = sess.run([val_images_batch, val_labels_batch])
                val_loss, val_acc = sess.run([loss, vgg_accuracy], 
                                             feed_dict={x_image:val_x, y_label:val_y})
                val_losses.append(val_loss)
                val_accs.append(val_acc)
            mean_loss = np.array(val_loss, dtype=np.float32).mean() # 求平均loss
            mean_acc = np.array(val_accs, dtype=np.float32).mean() # 求平均准确率
            print("step [%d] - val loss : %f, val accuracy : %f" %(i, mean_loss, mean_val))
        
        if (i%(epoch*10) == 0 and i > 0) or i == steps: # 每10个循环保存一次模型
            print("----save: 10 pre train model in step: %d"%(i))
            step_name = save_path + "model_of_step_%d.ckpt"%(i)
            saver.save(sess, step_name, global_step=i)
        
        if mean_acc > max_acc and mean_acc >0.5:
            max_acc = mean_acc
            best_model = save_path + "best_models_{}_{:.4f}.ckpt".format(i, max_acc)
            print("----save:{}".format(best_model))
            saver.save(sess, best_model)
        print('step %d finished'%(i))
