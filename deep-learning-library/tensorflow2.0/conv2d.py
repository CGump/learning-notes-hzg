# -*- coding: utf-8 -*-
# ================================================================
#
#   Editor      : PyCharm
#   File name   : conv2d.py
#   Author      : CGump
#   Email       : huangzhigang93@gmail.com
#   Created date: 2020/6/20 16:29
#
# ================================================================
import tensorflow as tf
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

img = Image.open("pxz.jpg")
img = np.array(img)


weigths = np.array([[[[1]], [[1]], [[1]]],
                    [[[1]], [[-5]], [[1]]],
                    [[[1]], [[1]], [[1]]]
                    ])
# weigths = np.array([[[[1/9, 1/9, 1/9], [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]]]])

weigths = tf.constant(weigths, dtype=tf.float32)
print(img.shape, weigths.shape)

# img_in = img[..., 1]
# img_in = tf.constant(img_in, dtype=tf.float32)
# img_in = tf.expand_dims(img_in, axis=0)
# img_in = tf.expand_dims(img_in, axis=-1)
# print(img_in.shape)

rgb_list = []
for i in range(0, 3):
    img_in = img[..., i]
    print(img_in.shape)
    img_in = tf.constant(img_in, dtype=tf.float32)
    img_in = tf.expand_dims(img_in, axis=0)
    img_in = tf.expand_dims(img_in, axis=-1)
    img_out = tf.nn.conv2d(img_in, weigths, strides=[1, 1, 1, 1], padding='SAME')
    rgb_list.append(img_out)

show_img = tf.concat(rgb_list, axis=-1)
print(show_img.shape)


# conv_img = tf.nn.conv2d(input=img_in, filters=weigths, strides=[1, 1, 1, 1], padding='SAME')
show_img = np.array(show_img[0], dtype=np.int)
# print(show_img.shape)
# print(conv_img.shape)
plt.title('conv')
plt.imshow(show_img)
plt.show()

