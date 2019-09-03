import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
print("check tensorflow version: ", tf.__version__)

import numpy as np
import matplotlib.pyplot as plt 

mnist = input_data.read_data_sets("MNIST_data", one_hot=True)
batch_size = 100
n_batch = mnist.train.num_examples // batch_size

x = tf.placeholder(tf.float32, [None, 784])
y = tf.placeholder(tf.float32, [None, 10])
keep_prob = tf.placeholder(tf.float32)

W_1 = tf.Variable(tf.truncated_normal([784, 500], stddev=0.1))
b_1 = tf.Variable(tf.zeros([500])+0.1)
L1 = tf.nn.tanh(tf.matmul(x, W_1) + b_1)
L1_drop = tf.nn.dropout(L1, keep_prob)

W_2 = tf.Variable(tf.truncated_normal([500, 300], stddev=0.1))
b_2 = tf.Variable(tf.zeros([300])+0.1)
L2 = tf.nn.tanh(tf.matmul(L1_drop, W_2) + b_2)
L2_drop = tf.nn.dropout(L2, keep_prob)

W_3 = tf.Variable(tf.truncated_normal([300, 10], stddev=0.1))
b_3 = tf.Variable(tf.zeros([10])+0.1)
prediction = tf.nn.softmax(tf.matmul(L2_drop, W_3) + b_3)

loss = tf.reduce_mean(tf.square(y - prediction))
train_step = tf.train.AdamOptimizer(0.001).minimize(loss)
init = tf.global_variables_initializer()

correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(prediction, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

with tf.Session() as sess:
    sess.run(init)
    for epoch in range(51):
        # sess.run(tf.assign(lr, 0.001 * (0.95 ** epoch)))
        for batch in range(n_batch):
            batch_xs,batch_ys = mnist.train.next_batch(batch_size)
            sess.run([train_step], feed_dict={x:batch_xs, y:batch_ys, keep_prob:1.0})
        test_acc = sess.run(accuracy, feed_dict={x:mnist.test.images, y:mnist.test.labels, keep_prob:1.0})
        train_acc = sess.run(accuracy, feed_dict={x:mnist.train.images, y:mnist.train.labels, keep_prob:1.0})
        print("Iter " + str(epoch) + ", Trainning Accuracy " + str(train_acc) + ", Testing Accuracy " + str(test_acc))
