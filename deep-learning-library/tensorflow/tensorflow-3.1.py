import tensorflow as tf
print("check tensorflow version: ", tf.__version__)
# tensorflow 线性回归

import numpy as np
import matplotlib.pyplot as plt 

# 使用numpy生成200个-0.5~0.5均匀分布的点，并通过np.newaxis进行扩维
x_data = np.linspace(-0.5, 0.5, 200)[:,np.newaxis]
noise = np.random.normal(0, 0.02, x_data.shape)
y_data = np.square(x_data) + noise

# 定义两个占位符placeholder
# 这里定义了占位符的形状，[None, 1]表示是一个任意行、1列的数组
x = tf.placeholder(tf.float32, [None, 1])
y = tf.placeholder(tf.float32, [None, 1])

# 构建简单的神经网络，实现回归问题
# 这里y是预测值，我们希望y能接近实际值y_data

# 构建神经网络中间层
# Weights_L1定义中间层权值，并进行参数值的随机初始化
# 权值是一个1行10列的向量，
# 1行是因为输入层是1个神经元，10是因为给中间层设置为10个神经元
Weights_L1 = tf.Variable(tf.random_normal([1, 10]))
# 中间层有10个神经元，偏置值列数为10，初始化时则全部为0
biases_L1 = tf.Variable(tf.zeros([1, 10]))
# 计算信号的总和
Wx_plus_b_L1 = tf.matmul(x,Weights_L1) + biases_L1
# 中间层输出，用tanh激活函数对总和进行拟合
L1 = tf.nn.tanh(Wx_plus_b_L1)

# 定义神经网络输出层
# 同样，中间层输出是10，输出层输出结果1，这里的矩阵规格为[10,1]
Weights_L2 = tf.Variable(tf.random_normal([10, 1]))
# 由于输出层只有一个神经元，因此偏置值只有一个
biases_L2 = tf.Variable(tf.zeros([1, 1]))
# 中间层的输出L1在这里即为输出层的输入，与神经元Weights_L2进行矩阵乘法
Wx_plus_b_L2 = tf.matmul(L1, Weights_L2) + biases_L2
# 预测结果
prediction = tf.nn.tanh(Wx_plus_b_L2)

# 定义损失函数和训练方法
loss = tf.reduce_mean(tf.square(y-prediction))
# 使用梯度下降法，并最小化loss
train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

with tf.Session() as sess:
    #变量初始化
    sess.run(tf.global_variables_initializer())
    for _ in range(2000):
        # 使用了feed操作对x和y的值进行传入
        sess.run(train_step, feed_dict={x:x_data, y:y_data})
    
    # 获得预测值
    prediction_value = sess.run(prediction, feed_dict={x:x_data})
    # 画图查看结果
    plt.figure()
    plt.scatter(x_data, y_data)  # 样本点
    plt.plot(x_data, prediction_value, 'r-', lw=5)  # 'r-' r表示红色，-表示实线
    plt.show()