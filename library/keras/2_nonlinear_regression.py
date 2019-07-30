import keras
import numpy as np
import matplotlib.pyplot as plt 
# Sequential按顺序构成的模型
from keras.models import Sequential
# Dense全连接层
from keras.layers import Dense,Activation
from keras.optimizers import SGD

# 使用numpy生成200个随机点，y_data为x的开方加上噪声
x_data = np.linspace(-0.5, 0.5, 200) #从[-0.5， 0.5]区间生成200个平均分布的点
noise = np.random.normal(0, 0.02, x_data.shape)
y_data = np.square(x_data) + noise

# 显示随机点
plt.scatter(x_data, y_data)

'''
由于线性模型中，对非线性数据的拟合结果依然为线性的，
所以单纯的1输入1输出不能完成所需的要求，
因此在输入和输出之间还需要添加一个隐藏层，进行非线性拟合
模型顺序：1-10-1
'''
# 构建一个顺序模型
model = Sequential()
# 在模型中添加一个10输出的全连接层
model.add(Dense(units=10, input_dim=1))
# 添加激活函数
# model.add(Activation('tanh'))
model.add(Activation('relu'))
# 添加输出层,这里可以不用添加输入，会根据上一层的输出进行匹配
model.add(Dense(units=1))
# 给输出层再添加一个激活函数
# model.add(Activation('tanh'))
model.add(Activation('relu'))
'''
在没有指定激活函数的前提下，默认的激活函数为a(x)=x
即为输入多少，经过激活函数输出是多少
对于非线性拟合，需要加入非线性的激活函数
激活函数可以直接在Dense层中添加，相应代码如下：
model.add(Dense(units=10, input_dim=1,activation='relu'))
'''
# 定义优化算法，把学习率改为0.3
sgd = SGD(lr=0.3)
# sgd:Stochastic gradient descent, 随机梯度下降法
# mse:Mean Squared Error, 均方误差
model.compile(optimizer=sgd, loss='mse')

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
print('W_hat:', W_hat, 'b_hat', b_hat)

# x_data输入网络中，得到预测值y_pred
y_pred = model.predict(x_data)

# 显示预测结果
plt.plot(x_data, y_pred, 'r-', lw=3)
plt.show()


