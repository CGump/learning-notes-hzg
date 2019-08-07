import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
print("check tensorflow version: ", tf.__version__)
# tensorflow 非线性回归 softmax函数用法 手写数字识别 

import numpy as np
import matplotlib.pyplot as plt 

# 输入是图像拉平为一维即28*28=784 输出是10个分类
# softmax是指数形式，其所有类的概率的和为1，然后分别进行单个概率的计算，
# 以e为底可以突出大数，过滤小数

# 载入数据(自动下载在在当前路径，其中“MINST_data”处可以改变路径)
mnist = input_data.read_data_sets("MNIST_data", one_hot=True)

# 定义每个批次的大小
batch_size = 100
# 计算一共有多少个批次
n_batch = mnist.train.num_examples // batch_size

# 定义两个placeholder
x = tf.placeholder(tf.float32, [None, 784])
y = tf.placeholder(tf.float32, [None, 10])

# 创建一个简单的神经网络
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))
prediction = tf.nn.softmax(tf.matmul(x, W) + b)

# 损失函数
loss = tf.reduce_mean(tf.square(y - prediction))
# 使用梯度下降法
train_step = tf.train.GradientDescentOptimizer(0.2).minimize(loss)

# 初始化
init = tf.global_variables_initializer()

# tf.equal是比较其中两个参数是否一致，相同True不同False
# tf.argmax是求y（标签）和预测值prediction中最大值是在那个位置，
# 因为标签是通过one_hot的方式来进行编码的，因此标签只有一个位置是1，其他都是0
# 所以这里用1来进行标签位置提取
# 结果存放在一个布尔型列表中
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(prediction, 1))
# 求准确率
# 该函数的作用是讲预测结果的布尔型列表转换为float32类型，再进行平均值计算
# 这里True对应1（float32），False对应0（float32）
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

with tf.Session() as sess:
    sess.run(init)
    for epoch in range(21):
        for batch in range(n_batch):
            # 获得一个批次的图片和标签，每个批次是100张,每个批次不重复
            batch_xs,batch_ys = mnist.train.next_batch(batch_size)
            sess.run(train_step, feed_dict={x:batch_xs, y:batch_ys})

        acc = sess.run(accuracy, feed_dict={x:mnist.test.images, y:mnist.test.labels})
        print("Iter " + str(epoch) + ".Testing Accuracy" + str(acc))

