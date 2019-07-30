import numpy as np 
# 从keras导入mnist的数据集（若无则会自动下载）
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense,Dropout,Convolution2D,MaxPooling2D,Flatten
# 常用的优化器Adam
from keras.optimizers import SGD,Adam
# 绘制网络结构 可能需要安装pydot和graphviz
from keras.utils.vis_utils import plot_model
import matplotlib.pyplot as plt


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


plot_model(model, to_file="model.png", show_shapes=True, show_layer_names=False, rankdir='TB')
plt.figure(figsize=(10,10))
img = plt.imread("model.png")
plt.show(img)
plt.axis('off')
plt.show()