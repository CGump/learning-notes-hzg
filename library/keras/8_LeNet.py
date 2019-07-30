import numpy as np 
# 从keras导入mnist的数据集（若无则会自动下载）
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense,Dropout,Convolution2D,MaxPooling2D,Flatten
# 常用的优化器Adam
from keras.optimizers import SGD,Adam

(x_train, y_train),(x_test, y_test) = mnist.load_data()

# 数据格式转换 (60000,28,28) -> (60000,28,28,1)
x_train = x_train.reshape(-1, 28, 28, 1)/255.0 #设置成-1会直接把shape[1]和[2]相乘，也可以直接设置为784
x_test = x_test.reshape(-1, 28, 28, 1)/255.0
# 将标签转为one hot格式
y_train = np_utils.to_categorical(y_train, num_classes=10)
y_test = np_utils.to_categorical(y_test, num_classes=10)


# 定义顺序模型（注意这里是CNN的顺序模型，模型从上到下只有一条线，没有分支）
model = Sequential()

# 第一个卷积层
model.add(Convolution2D(
    input_shape=(28,28,1), # 28*28*1，数据集的图片是单通道的
    filters=32,
    kernel_size=5,
    strides=1,
    padding='same',
    activation='relu'
))
'''
定义卷积层
    input_shape 输入平面
    filters 卷积核/滤波器个数
    kernel_size 卷积窗口大小
    strides 步长
    padding padding方式 same/valid两种
    activation 激活函数
'''
# 第一个池化层
model.add(MaxPooling2D(
    pool_size=2,
    strides=2,
    padding='same'
))

# 第二个卷积层
model.add(Convolution2D(64, 5, strides=1, padding='same', activation='relu'))
# 第二个池化层
model.add(MaxPooling2D(2, 2, padding='same'))
# 把第二个池化层的输出扁平化为1维
model.add(Flatten())
# 第一个全连接层
model.add(Dense(1024, activation='relu'))
# Dropout
model.add(Dropout(0.5))
# 第二个全连接层
model.add(Dense(10, activation='softmax'))

# 设置优化器，常用Adam
adam = Adam(lr=1e-4)

# 定义优化器，loss function，训练过程中计算准确率
model.compile(optimizer=adam, loss='categorical_crossentropy', metrics=['accuracy'])

# 通过fit方法进行训练模型
model.fit(x_train, y_train, batch_size=64, epochs=10)

# 评估模型
loss,accuracy = model.evaluate(x_test, y_test)

print('test loss',loss)
print('accuracy', accuracy)


'''
每一个迭代周期，都要把训练集中batch数全部迭代完成
比如60000张图，batch_size=64
那么一个迭代周期计算的次数为60000/64
这里跟yolov3中食材识别是一样的
'''

# 保存模型
model.save('model.h5')
'''
通过model.save进行保存模型
函数中为路径+名字+后缀，如果只有名字则默认当前目录下保存
保存格式为HDF5文件，需要pip install h5py

'''