import numpy as np 
# 从keras导入mnist的数据集（若无则会自动下载）
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense,Dropout
from keras.optimizers import SGD
#导入正则化函数
from keras.regularizers import l2
# 载入数据
(x_train, y_train),(x_test, y_test) = mnist.load_data()

# 数据格式转换 (60000,28,28) -> (60000,784)
x_train = x_train.reshape(x_train.shape[0], -1)/255.0 #设置成-1会直接把shape[1]和[2]相乘，也可以直接设置为784
x_test = x_test.reshape(x_test.shape[0], -1)/255.0
# 将标签转为one hot格式
y_train = np_utils.to_categorical(y_train, num_classes=10)
y_test = np_utils.to_categorical(y_test, num_classes=10)

# 创建模型，输入784个神经元，输出10个神经元（即为类别）
model= Sequential([
    Dense(units=200, input_dim=784, bias_initializer='one', activation='tanh', kernel_regularizer=l2(0.0003)),
    Dense(units=100, bias_initializer='one', activation='tanh', kernel_regularizer=l2(0.0003)),
    Dense(units=10, bias_initializer='one', activation='softmax', kernel_regularizer=l2(0.0003)),
])
'''
正则化函数分为l1和l2，一共有三种正则化参数，这里只添加了一种。
什么时候加正则化？
当模型对于数据集来说过于复杂，加上正则化会效果好一点
'''

# 重新设置学习速率
sgd = SGD(lr=0.2)

# 定义优化器，loss function，训练过程中计算准确率
model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])

# 通过fit方法进行训练模型
model.fit(x_train, y_train, batch_size=32, epochs=10)

# 评估模型
loss,accuracy = model.evaluate(x_test, y_test)

print('test loss',loss)
print('accuracy', accuracy)
