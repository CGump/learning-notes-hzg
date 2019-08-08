import tensorflow as tf
print("check tensorflow version: ", tf.__version__)

a = [[0.15, 0.80, 0.05],[0.04, 0.36, 0.60]]
b = [[0.15, 0.60, 0.05],[0.05, 0.36, 0.70]]
with tf.Session() as sess:
    print(sess.run(tf.equal(a, b)))    