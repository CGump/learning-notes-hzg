import numpy as np 
# 从keras导入mnist的数据集（若无则会自动下载）
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD

# 载入数据
(x_train, y_train),(x_test, y_test) = mnist.load_data()

# 打印训练数据的格式
print('x_shape:', x_train.shape)
print('y_shape:', y_train.shape)
'''
x_shape: (60000, 28, 28)
y_shape: (60000,)
'''
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
model.compile(optimizer=sgd, loss='mse', metrics=['accuracy'])

# 通过fit方法进行训练模型
model.fit(x_train, y_train, batch_size=32, epochs=10)
'''
MNIST数据集总共60000张图片
batch_size=32表示每1次训练使用其中32张图片进行，直到60000张图片训练完，成为1个周期
epochs=10表示以上的batch_size迭代循环10个周期
'''
# 评估模型
loss,accuracy = model.evaluate(x_test, y_test)

print('test loss',loss)
print('accuracy', accuracy)


'''Epoch 1/10
2019-07-03 16:11:42.698800: I tensorflow/core/platform/cpu_feature_guard.cc:140] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX AVX2
60000/60000 [==============================] - 2s 28us/step - loss: 0.0378 - acc: 0.7732
Epoch 2/10
60000/60000 [==============================] - 1s 23us/step - loss: 0.0204 - acc: 0.8800
Epoch 3/10
60000/60000 [==============================] - 1s 22us/step - loss: 0.0178 - acc: 0.8920
Epoch 4/10
60000/60000 [==============================] - 1s 22us/step - loss: 0.0165 - acc: 0.8990
Epoch 5/10
60000/60000 [==============================] - 1s 22us/step - loss: 0.0157 - acc: 0.9030
Epoch 6/10
60000/60000 [==============================] - 1s 22us/step - loss: 0.0151 - acc: 0.9064
Epoch 7/10
60000/60000 [==============================] - 1s 22us/step - loss: 0.0147 - acc: 0.9086
Epoch 8/10
60000/60000 [==============================] - 1s 22us/step - loss: 0.0143 - acc: 0.9110
Epoch 9/10
60000/60000 [==============================] - 1s 22us/step - loss: 0.0140 - acc: 0.9124
Epoch 10/10
60000/60000 [==============================] - 1s 22us/step - loss: 0.0138 - acc: 0.9137
10000/10000 [==============================] - 0s 11us/step
test loss 0.013063172332709655
accuracy 0.9185
'''