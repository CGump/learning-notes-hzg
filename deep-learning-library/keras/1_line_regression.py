import keras
import numpy as np
import matplotlib.pyplot as plt 
# Sequential按顺序构成的模型
from keras.models import Sequential
# Dense全连接层
from keras.layers import Dense

# 使用numpy生成100个随机点
x_data = np.random.rand(100)
noise = np.random.normal(0, 0.01, x_data.shape)
W, b = [0.1, 0.2]
y_data = x_data * W + b + noise

# 显示随机点
plt.scatter(x_data, y_data)


# 构建一个顺序模型
model = Sequential()
# 在模型中添加一个全连接层
model.add(Dense(units=1, input_dim=1))
'''
全连接层 Dense()类中初始化参数
Dense(units=1, input_dim=1)，units=1表示输出是1维度的，input_dim=1表示输入为1
'''
# sgd:Stochastic gradient descent, 随机梯度下降法
# mse:Mean Squared Error, 均方误差
model.compile(optimizer='sgd', loss='mse')
'''
model.compile 设置优化器和loss层
其中优化器optimizer='sgd'使用随机梯度下降法，loss='mse'为使用均方误差
'''

# 训练3001个批次
for step in range(3001):
    # 每次训练一个批次
    cost = model.train_on_batch(x_data, y_data)
    '''
    tran_on_batch：按照批次训练，由于这里数据只有100个，所以就直接全部作为1个批次放入
    '''
    # 每500个batch打印一次cost值
    if step % 500 == 0:
        print('cost:', cost)

# 打印权值和偏置值
W_hat, b_hat = model.layers[0].get_weights()
print('W:',W,'b:',b, 'W_hat:', W_hat, 'b_hat', b_hat)

# x_data输入网络中，得到预测值y_pred
y_pred = model.predict(x_data)

# 显示预测结果
plt.plot(x_data, y_pred, 'r-', lw=3)
plt.show()

'''
cost: 0.37334538
cost: 0.005175937
cost: 0.0014455402
cost: 0.00045425215
cost: 0.00019083497
cost: 0.00012083635
cost: 0.00010223536
W: 0.1 b: 0.2 W_hat: [[0.09540579]] b_hat [0.2019255]

这里W_hat和b_hat近似于设置的W和b

github desktop test in 10.34 2019/7/8

github desktop test in 10.36 2019/7/8
'''