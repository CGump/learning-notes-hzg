import tensorflow as tf
print("check tensorflow version: ", tf.__version__)
# tensorflow Fetch，Feed

# Fetch 可以在会话里面执行多个op，并得到结果
# 定义三个常量op
input1 = tf.constant(3.0)
input2 = tf.constant(2.0)
input3 = tf.constant(5.0)

add = tf.add(input2, input3)
mul = tf.multiply(input1, add)

with tf.Session() as sess:
    # 将两个op通过[]的形式依次框起后，放入run()中即可同时计算两个op
    # 并输出结果至result，这个操作成为Fetch
    result = sess.run([mul, add])
    print(result)

# Feed
# 创建占位符，可以在运行的时候再把数值导入
input1 = tf.placeholder(tf.float32)
input2 = tf.placeholder(tf.float32)
output = tf.multiply(input1, input2)

with tf.Session() as sess:
    # 对占位符的数值传入，是使用python中字典的形式
    # feed={}
    print(sess.run(output, feed_dict={input1:[7.], input2:[2.]}))