import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
print("check tensorflow version: ", tf.__version__)
# tensorflow dropout

import numpy as np
import matplotlib.pyplot as plt 

mnist = input_data.read_data_sets("MNIST_data", one_hot=True)
batch_size = 100
n_batch = mnist.train.num_examples // batch_size

x = tf.placeholder(tf.float32, [None, 784])
y = tf.placeholder(tf.float32, [None, 10])
# 增加隐藏层，再定义一个占位符
keep_prob = tf.placeholder(tf.float32)

# 创建一个简单的神经网络，并进行初始化w和b
# 一般采用正态分布的方式进行初始化
W_1 = tf.Variable(tf.truncated_normal([784, 2000], stddev=0.1))
b_1 = tf.Variable(tf.zeros([2000])+0.1)
L1 = tf.nn.tanh(tf.matmul(x, W_1) + b_1)
# 定义L1的dropout,这里keep_prob是用于控制多少比例的神经元不工作
L1_drop = tf.nn.dropout(L1, keep_prob)

W_2 = tf.Variable(tf.truncated_normal([2000, 2000], stddev=0.1))
b_2 = tf.Variable(tf.zeros([2000])+0.1)
L2 = tf.nn.tanh(tf.matmul(L1_drop, W_2) + b_2)
L2_drop = tf.nn.dropout(L2, keep_prob)

W_3 = tf.Variable(tf.truncated_normal([2000, 1000], stddev=0.1))
b_3 = tf.Variable(tf.zeros([1000])+0.1)
L3 = tf.nn.tanh(tf.matmul(L2_drop, W_3) + b_3)
L3_drop = tf.nn.dropout(L3, keep_prob)

W_4 = tf.Variable(tf.zeros([1000, 10]))
b_4 = tf.Variable(tf.zeros([10]))
prediction = tf.nn.softmax(tf.matmul(L3_drop, W_4) + b_4)


# 损失函数
loss = tf.reduce_mean(tf.square(y - prediction))
# 使用梯度下降法
train_step = tf.train.GradientDescentOptimizer(0.2).minimize(loss)

# 初始化
init = tf.global_variables_initializer()

correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(prediction, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

with tf.Session() as sess:
    sess.run(init)
    for epoch in range(31):
        for batch in range(n_batch):
            # 获得一个批次的图片和标签，每个批次是100张,每个批次不重复
            batch_xs,batch_ys = mnist.train.next_batch(batch_size)
            sess.run([train_step], feed_dict={x:batch_xs, y:batch_ys, keep_prob:0.7})
            # print(see_cp)
        test_acc = sess.run(accuracy, feed_dict={x:mnist.test.images, y:mnist.test.labels, keep_prob:0.7})
        train_acc = sess.run(accuracy, feed_dict={x:mnist.train.images, y:mnist.train.labels, keep_prob:1.0})
        print("Iter " + str(epoch) + ", Trainning Accuracy " + str(train_acc) + ", Testing Accuracy " + str(test_acc))


'''
不使用dropout的情况下训练，可以看出：训练收敛很快，精度很高，
但是训练的准确率接近1.0而测试准确率只有0.97，此时，模型过拟合
Iter 0, Trainning Accuracy 0.9145091, Testing Accuracy 0.9178
Iter 1, Trainning Accuracy 0.9353091, Testing Accuracy 0.9325
Iter 2, Trainning Accuracy 0.9468727, Testing Accuracy 0.9398
Iter 3, Trainning Accuracy 0.9547455, Testing Accuracy 0.9452
Iter 4, Trainning Accuracy 0.96196365, Testing Accuracy 0.9496
Iter 5, Trainning Accuracy 0.9669091, Testing Accuracy 0.9518
Iter 6, Trainning Accuracy 0.9711818, Testing Accuracy 0.9545
Iter 7, Trainning Accuracy 0.97474545, Testing Accuracy 0.9559
Iter 8, Trainning Accuracy 0.9769818, Testing Accuracy 0.9573
Iter 9, Trainning Accuracy 0.9798, Testing Accuracy 0.9594
Iter 10, Trainning Accuracy 0.9816727, Testing Accuracy 0.9602
Iter 11, Trainning Accuracy 0.98350906, Testing Accuracy 0.9606
Iter 12, Trainning Accuracy 0.9850909, Testing Accuracy 0.9613
Iter 13, Trainning Accuracy 0.9864, Testing Accuracy 0.9616
Iter 14, Trainning Accuracy 0.9876364, Testing Accuracy 0.9628
Iter 15, Trainning Accuracy 0.9883636, Testing Accuracy 0.9629
Iter 16, Trainning Accuracy 0.9891091, Testing Accuracy 0.9634
Iter 17, Trainning Accuracy 0.9899091, Testing Accuracy 0.9648
Iter 18, Trainning Accuracy 0.9905273, Testing Accuracy 0.9648
Iter 19, Trainning Accuracy 0.99114543, Testing Accuracy 0.9656
Iter 20, Trainning Accuracy 0.9917091, Testing Accuracy 0.9657
Iter 21, Trainning Accuracy 0.9921091, Testing Accuracy 0.9661
Iter 22, Trainning Accuracy 0.9924, Testing Accuracy 0.9666
Iter 23, Trainning Accuracy 0.99258184, Testing Accuracy 0.9662
Iter 24, Trainning Accuracy 0.9929818, Testing Accuracy 0.9668
Iter 25, Trainning Accuracy 0.9932909, Testing Accuracy 0.9669
Iter 26, Trainning Accuracy 0.9936727, Testing Accuracy 0.9676
Iter 27, Trainning Accuracy 0.9939455, Testing Accuracy 0.968
Iter 28, Trainning Accuracy 0.9942727, Testing Accuracy 0.9675
Iter 29, Trainning Accuracy 0.9945273, Testing Accuracy 0.9677
Iter 30, Trainning Accuracy 0.99463636, Testing Accuracy 0.9678


使用dropout后，训练收敛变慢，过拟合现象减弱
Iter 0, Trainning Accuracy 0.8772, Testing Accuracy 0.8518
Iter 1, Trainning Accuracy 0.89823633, Testing Accuracy 0.8679
Iter 2, Trainning Accuracy 0.90934545, Testing Accuracy 0.8852
Iter 3, Trainning Accuracy 0.9165091, Testing Accuracy 0.8922
Iter 4, Trainning Accuracy 0.9210727, Testing Accuracy 0.8963
Iter 5, Trainning Accuracy 0.9252, Testing Accuracy 0.9002
Iter 6, Trainning Accuracy 0.9283818, Testing Accuracy 0.9016
Iter 7, Trainning Accuracy 0.93045455, Testing Accuracy 0.9037
Iter 8, Trainning Accuracy 0.9337091, Testing Accuracy 0.9084
Iter 9, Trainning Accuracy 0.935, Testing Accuracy 0.9069
Iter 10, Trainning Accuracy 0.9375091, Testing Accuracy 0.9127
Iter 11, Trainning Accuracy 0.9391636, Testing Accuracy 0.9141
Iter 12, Trainning Accuracy 0.9404, Testing Accuracy 0.9132
Iter 13, Trainning Accuracy 0.94216365, Testing Accuracy 0.9163
Iter 14, Trainning Accuracy 0.9435273, Testing Accuracy 0.917
Iter 15, Trainning Accuracy 0.9444364, Testing Accuracy 0.9187
Iter 16, Trainning Accuracy 0.94525456, Testing Accuracy 0.9194
Iter 17, Trainning Accuracy 0.94665456, Testing Accuracy 0.9207
Iter 18, Trainning Accuracy 0.9476909, Testing Accuracy 0.9232
Iter 19, Trainning Accuracy 0.94903636, Testing Accuracy 0.9211
Iter 20, Trainning Accuracy 0.95025456, Testing Accuracy 0.9253
Iter 21, Trainning Accuracy 0.95094544, Testing Accuracy 0.923
Iter 22, Trainning Accuracy 0.9518909, Testing Accuracy 0.9283
Iter 23, Trainning Accuracy 0.9530182, Testing Accuracy 0.9257
Iter 24, Trainning Accuracy 0.954, Testing Accuracy 0.9273
Iter 25, Trainning Accuracy 0.9545636, Testing Accuracy 0.9292
Iter 26, Trainning Accuracy 0.9557818, Testing Accuracy 0.926
Iter 27, Trainning Accuracy 0.9563636, Testing Accuracy 0.9297
Iter 28, Trainning Accuracy 0.9566909, Testing Accuracy 0.9303
Iter 29, Trainning Accuracy 0.95721817, Testing Accuracy 0.9303
Iter 30, Trainning Accuracy 0.9580909, Testing Accuracy 0.9332

'''