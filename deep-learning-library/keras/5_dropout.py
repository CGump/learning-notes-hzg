import numpy as np 
# 从keras导入mnist的数据集（若无则会自动下载）
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense,Dropout
from keras.optimizers import SGD

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
    Dense(units=200, input_dim=784, bias_initializer='one', activation='tanh'),
    Dropout(0.4),
    Dense(units=100, bias_initializer='one', activation='tanh'),
    Dropout(0.4),
    Dense(units=10, bias_initializer='one', activation='softmax'),
])
'''
dropout加在输出之前，因此需要新建一个隐藏层
softmax一般放在神经网络的最后一层（输出层）

上面创建模型的方式与之前model.add是相同的
model.add(Dense(...))
model.add(Dense(...))
同样的，在配置各层时只需要知道第一层的输入和输出，后续的输入均会自动匹配为前一层的输出

dropout可以看成为一层
其中的0.4表示让40%的神经元不工作

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
