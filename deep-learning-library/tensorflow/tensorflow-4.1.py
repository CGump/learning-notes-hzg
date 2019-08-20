import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
print("check tensorflow version: ", tf.__version__)
# tensorflow 交叉熵 

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

train_step = tf.train.GradientDescentOptimizer(0.2).minimize(loss)

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




'''
# 使用二次代价函数
Iter 0.Testing Accuracy0.8305
Iter 1.Testing Accuracy0.8708
Iter 2.Testing Accuracy0.8819
Iter 3.Testing Accuracy0.8886
Iter 4.Testing Accuracy0.8944
Iter 5.Testing Accuracy0.8969
Iter 6.Testing Accuracy0.8986
Iter 7.Testing Accuracy0.9021
Iter 8.Testing Accuracy0.903
Iter 9.Testing Accuracy0.9047
Iter 10.Testing Accuracy0.9064
Iter 11.Testing Accuracy0.9072
Iter 12.Testing Accuracy0.9083
Iter 13.Testing Accuracy0.9096
Iter 14.Testing Accuracy0.9099
Iter 15.Testing Accuracy0.9106
Iter 16.Testing Accuracy0.9114
Iter 17.Testing Accuracy0.9119
Iter 18.Testing Accuracy0.9136
Iter 19.Testing Accuracy0.9135
Iter 20.Testing Accuracy0.9139


#使用交叉熵
Iter 0.Testing Accuracy0.8443
Iter 1.Testing Accuracy0.8947
Iter 2.Testing Accuracy0.9019
Iter 3.Testing Accuracy0.9065
Iter 4.Testing Accuracy0.9087
Iter 5.Testing Accuracy0.9111
Iter 6.Testing Accuracy0.9129
Iter 7.Testing Accuracy0.9132
Iter 8.Testing Accuracy0.9148
Iter 9.Testing Accuracy0.9171
Iter 10.Testing Accuracy0.9185
Iter 11.Testing Accuracy0.918
Iter 12.Testing Accuracy0.9184
Iter 13.Testing Accuracy0.9199
Iter 14.Testing Accuracy0.9189
Iter 15.Testing Accuracy0.9214
Iter 16.Testing Accuracy0.9204
Iter 17.Testing Accuracy0.9209
Iter 18.Testing Accuracy0.9212
Iter 19.Testing Accuracy0.9223
Iter 20.Testing Accuracy0.9217

'''