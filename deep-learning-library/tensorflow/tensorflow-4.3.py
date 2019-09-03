import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
print("check tensorflow version: ", tf.__version__)
# tensorflow 优化器

import numpy as np
import matplotlib.pyplot as plt 

mnist = input_data.read_data_sets("MNIST_data", one_hot=True)

batch_size = 100
n_batch = mnist.train.num_examples // batch_size

x = tf.placeholder(tf.float32, [None, 784])
y = tf.placeholder(tf.float32, [None, 10])

W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))
prediction = tf.nn.softmax(tf.matmul(x, W) + b)

# 损失函数
# loss = tf.reduce_mean(tf.square(y - prediction)) 使用二次代价函数
# 这里输出层已经经过一次softmax，对于已经softmax转换过的预测值不能再使用这个函数！！！
loss =tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=prediction)) #使用交叉熵

# train_step = tf.train.GradientDescentOptimizer(0.2).minimize(loss)
# 优化器主要有：
# tf.train.GradientDescentOptimizer
# tf.train.AdadeltaOptimizer
# tf.train.AdagradDAOptimizer
# tf.train.MomentumOptimizer
# tf.train.AdamOptimizer
# tf.train.FtrlOptimizer
# tf.train.ProximalGradientDescentOptimizer
# tf.train.ProximalAdagradOptimizer
# tf.train.RMSPropOptimizer
# 最好所有的优化器都试一下
train_step = tf.train.AdamOptimizer(1e-2).minimize(loss) # 使用Adam激活函数


init = tf.global_variables_initializer()

correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(prediction, 1))
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

