import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.contrib.tensorboard.plugins import projector
print("check tensorflow version: ", tf.__version__)
# tensorflow 卷积神经网络
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
# 每个批次大小
batch_size = 100
# 一共计算的批次数 总数/批次大小
n_batch = mnist.train.num_examples // batch_size

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

x_image = tf.placeholder(tf.float32, [None, 224, 224, 3])
y_label = tf.placeholder(tf.float32, [None, 80])  # 假设分80类

#输入 224*224*3
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

# 第三层：4*conv+1*pool
conv3_1 = conv_layer(pool2, [3, 3, 128, 256], 1, 1, [256], 'conv3-1')
conv3_2 = conv_layer(conv3_1, [3, 3, 256, 256], 1, 1, [256], 'conv3-2')
conv3_3 = conv_layer(conv3_2, [3, 3, 256, 256], 1, 1, [256], 'conv3-3')
conv3_4 = conv_layer(conv3_3, [3, 3, 256, 256], 1, 1, [256], 'conv3-4')
pool3 = max_pool_layer(conv3_4, [1, 2, 2, 1], 2, 2, 'pool3')

# 第四层：4*conv+1*pool
conv4_1 = conv_layer(pool3, [3, 3, 128, 256], 1, 1, [256], 'conv4-1')
