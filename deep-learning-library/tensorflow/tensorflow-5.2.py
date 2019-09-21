import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
print("check tensorflow version: ", tf.__version__)
# tensorflow tensorboard 网络运行参数查看
# 每运行一次需要把前一次logs文件夹中的tensorboard缓存删除

import numpy as np
import matplotlib.pyplot as plt 

mnist = input_data.read_data_sets("MNIST_data", one_hot=True)

# 定义每个批次的大小
batch_size = 100
# 计算一共有多少个批次
n_batch = mnist.train.num_examples // batch_size

# 定义一个分析函数
def variable_summarie(var):
    with tf.name_scope('summaries'): # 大命名空间，计算一系列的参数
        mean = tf.reduce_mean(var)  # 计算参数平均值
        tf.summary.scalar('mean', mean) # 给计算的参数命名为平均值
        with tf.name_scope('stddev'):  #小命名空间，计算标准差
            stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean))) # 计算标准差
        tf.summary.scalar('stddev', stddev) # 命名为标准差
        tf.summary.scalar('max', tf.reduce_max(var)) # 计算并命名为最大值
        tf.summary.scalar('min', tf.reduce_min(var)) # 计算并命名为最小值
        tf.summary.histogram('histogram', var) # 统计直方图

# 使用tensorboard时需要添加一个命名空间
# 命名空间
with tf.name_scope('input'):
    # 定义两个placeholder
    x = tf.placeholder(tf.float32, [None, 784], name='x-input')
    y = tf.placeholder(tf.float32, [None, 10], name='y-input')

# 创建参数的命名空间，在layer网络层的命名空间中嵌套的一个命名空间
with tf.name_scope('layer'):
    with tf.name_scope('wights'):
        W = tf.Variable(tf.zeros([784, 10]), name='W')
        variable_summarie(W) # 分析权值和偏置
    with tf.name_scope('biases'):
        b = tf.Variable(tf.zeros([10]), name='b')
        variable_summarie(b) # 分析权值和偏重
    # 拆分预测值的过程
    # 拆分->prediction = tf.nn.softmax(tf.matmul(x, W) + b)
    with tf.name_scope('wx_plus_b'):
        wx_plus_b = tf.matmul(x, W) + b
    with tf.name_scope('softmax'):
        prediction = tf.nn.softmax(wx_plus_b)


with tf.name_scope('loss'):
    # 损失函数
    loss = tf.reduce_mean(tf.square(y - prediction))
    tf.summary.scalar('loss', loss) # 分析一下loss
with tf.name_scope('train'):
    # 使用梯度下降法
    train_step = tf.train.GradientDescentOptimizer(0.2).minimize(loss)

init = tf.global_variables_initializer()
with tf.name_scope('accuracy'):
    with tf.name_scope('correct_prediction'):
        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(prediction, 1))
    with tf.name_scope('accuracy'):
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        tf.summary.scalar('accuracy', accuracy)

# 合并所有的summary
merged = tf.summary.merge_all()

with tf.Session() as sess:
    sess.run(init)
    # 添加tensorboard模型结构的存放目录
    writer = tf.summary.FileWriter('logs/', sess.graph)
    for epoch in range(51):
        for batch in range(n_batch):
            # 获得一个批次的图片和标签，每个批次是100张,每个批次不重复
            batch_xs,batch_ys = mnist.train.next_batch(batch_size)
            summary,_ = sess.run([merged, train_step], feed_dict={x:batch_xs, y:batch_ys}) # 把合并后的所有指标加在训练上

        writer.add_summary(summary, epoch) # 把summary记录下来
        acc = sess.run(accuracy, feed_dict={x:mnist.test.images, y:mnist.test.labels})
        print("Iter " + str(epoch) + ".Testing Accuracy" + str(acc))

