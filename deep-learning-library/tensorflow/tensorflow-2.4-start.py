import tensorflow as tf
print("check tensorflow version: ", tf.__version__)
# tensorflow 简单示例（线性回归）

import numpy as np

# 使用numpy生成100个随机点
x_data = np.random.rand(100)
y_data = x_data*0.1 + 0.2

# 构造一个线性模型
# 这里赋值时用了浮点的表示方式(0.)，
# 意思为该变量的格式为浮点，我们后面也需要用到小数
# 这里进行b、k与y_data中的斜率和偏置进行拟合
# 这里的y即为预测值
b = tf.Variable(0.)
k = tf.Variable(0.)
y = k*x_data + b

# 创建二次代价函数
# 这里即为损失函数，计算均方差的损失，先用y_data-y进行平方，
# 然后求和后求均值
loss = tf.reduce_mean(tf.square(y_data - y))
# 定义一个梯度下降法来进行训练的优化器
# 这里使用经典的GradientDescentOptimizer，给与一个学习率（下降速度）0.2
optimizer = tf.train.GradientDescentOptimizer(0.2)
# 最小化代价函数
# 训练的目的就是最小化loss，使得计算的结果更接近于真实值
train = optimizer.minimize(loss)

# 初始化变量
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    for step in range(401):
        '''
        每一次迭代都需要run一次train，此时train会求loss的最小值
        而loss是y_data和y的差值，y_data是确定的值，
        而y是由k、b决定，所以影响loss的值的关键就是k、b
        k、b是tensorflow中的两个变量，使用梯度下降法的方法改变k和b
        从而使得loss值变小，使得k、b接近y_data中的0.1和0.2
        '''
        sess.run(train)
        if step%20 == 0:
            # 每20次打印出k、b的值
            print(step, sess.run([k, b]))