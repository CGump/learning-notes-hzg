import numpy as np 
# 从keras导入mnist的数据集（若无则会自动下载）
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense
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
    Dense(units=10, input_dim=784, bias_initializer='one', activation='softmax')
])
# 重新设置学习速率
sgd = SGD(lr=0.2)

# 定义优化器，loss function，训练过程中计算准确率
model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])
'''
将loss方法的方差mse改为交叉熵categorical_crossentropy
使用交叉熵，模型的收敛速度比较快
适用于分类问题
能够快速收敛，但是提升不多
'''
# 通过fit方法进行训练模型
model.fit(x_train, y_train, batch_size=32, epochs=10)

# 评估模型
loss,accuracy = model.evaluate(x_test, y_test)

print('test loss',loss)
print('accuracy', accuracy)



'''
Epoch 1/10
60000/60000 [==============================] - 2s 27us/step - loss: 0.3783 - acc: 0.8926
Epoch 2/10
60000/60000 [==============================] - 1s 21us/step - loss: 0.3028 - acc: 0.9141
Epoch 3/10
60000/60000 [==============================] - 1s 20us/step - loss: 0.2894 - acc: 0.9181
Epoch 4/10
60000/60000 [==============================] - 1s 20us/step - loss: 0.2827 - acc: 0.9204
Epoch 5/10
60000/60000 [==============================] - 1s 21us/step - loss: 0.2778 - acc: 0.9228
Epoch 6/10
60000/60000 [==============================] - 1s 21us/step - loss: 0.2747 - acc: 0.9240
Epoch 7/10
60000/60000 [==============================] - 1s 21us/step - loss: 0.2708 - acc: 0.9246
Epoch 8/10
60000/60000 [==============================] - 1s 20us/step - loss: 0.2689 - acc: 0.9248
Epoch 9/10
60000/60000 [==============================] - 1s 20us/step - loss: 0.2671 - acc: 0.9260
Epoch 10/10
60000/60000 [==============================] - 1s 20us/step - loss: 0.2647 - acc: 0.9260
10000/10000 [==============================] - 0s 11us/step
test loss 0.27744944233596325
accuracy 0.9226
'''