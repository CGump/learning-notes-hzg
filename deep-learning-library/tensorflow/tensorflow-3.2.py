import tensorflow as tf
print("check tensorflow version: ", tf.__version__)
# tensorflow 非线性回归 softmax函数用法 手写数字数据集 LeNet5搭建

import numpy as np
import matplotlib.pyplot as plt 

# 输入是图像拉平为一维即28*28=784 输出是10个分类
# softmax是指数形式，其所有类的概率的和为1，然后分别进行单个概率的计算，
# 以e为底可以突出大数，过滤小数