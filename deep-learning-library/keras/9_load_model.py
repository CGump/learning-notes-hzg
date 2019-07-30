import numpy as np 
# 从keras导入mnist的数据集（若无则会自动下载）
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense,Dropout,Convolution2D,MaxPooling2D,Flatten
# 常用的优化器Adam
from keras.optimizers import SGD,Adam
# 载入模型需要引入的函数
from keras.models import load_model

# 载入数据
(x_train, y_train),(x_test, y_test) = mnist.load_data()

# 数据格式转换 (60000,28,28) -> (60000,28,28,1)
x_train = x_train.reshape(-1, 28, 28, 1)/255.0 #设置成-1会直接把shape[1]和[2]相乘，也可以直接设置为784
x_test = x_test.reshape(-1, 28, 28, 1)/255.0
# 将标签转为one hot格式
y_train = np_utils.to_categorical(y_train, num_classes=10)
y_test = np_utils.to_categorical(y_test, num_classes=10)

# 载入模型
model = load_model('model.h5')
'''
通过load_model函数进行模型的读取
载入模型后，还可以继续通过fit函数对模型进行训练
model.fit(x_train, y_train, batch_size=64, epochs=10)
'''

# 评估模型
loss,accuracy = model.evaluate(x_test, y_test)

print('test loss',loss)
print('accuracy', accuracy)

# 保存参数，载入参数
model.save_weights('my_model_weights.h5')
model.load_weights('my_model_weights.h5')
# 保存网络结构，载入网络结构
from keras.models import model_from_json
json_string = model.to_json()
model = model_from_json(json_string)

print(json_string)

'''
也可以单独保存参数和网络结构
通过model_from_json可以将网络结构保存、打印出来
'''
