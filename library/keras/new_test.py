import keras as K

model = K.models.Sequential()

conv1 = K.layers.Convolution2D(input_shape=(28,28,1),filters=32,kernel_size=5,strides=1,padding='same',activation='relu')
pooling1 = K.layers.MaxPooling2D(2,2,'same')

model.add(conv1)
model.add(pooling1)

print(model)

K.utils.print_summary(model)

'''
model.summary()：打印出模型概况，它实际调用的是keras.utils.print_summary

model.get_config():返回包含模型配置信息的Python字典。模型也可以从它的config信息中重构回去

model.get_layer()：依据层名或下标获得层对象

model.get_weights()：返回模型权重张量的列表，类型为numpy array

model.set_weights()：从numpy array里将权重载入给模型，要求数组具有与model.get_weights()相同的形状。

model.to_json：返回代表模型的JSON字符串，仅包含网络结构，不包含权值。可以从JSON字符串中重构原模型：

model.save_weights(filepath)：将模型权重保存到指定路径，文件类型是HDF5（后缀是.h5）

model.load_weights(filepath, by_name=False)：从HDF5文件中加载权重到当前模型中, 默认情况下模型的结构将保持不变。如果想将权重载入不同的模型（有些层相同）中，则设置by_name=True，只有名字匹配的层才会载入权重

'''

# 今天教倩宝宝用github