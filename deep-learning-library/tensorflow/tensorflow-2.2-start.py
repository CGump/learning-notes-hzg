import tensorflow as tf
print("check tensorflow version: ", tf.__version__)
# tensorflow 变量的应用

# 定义一个变量
x = tf.Variable([1,2])
# 定义一个常量
a = tf.constant([3,3])
# 增加一个减法op
sub = tf.subtract(x, a)
# 增加一个加法op
add = tf.add(x, sub)

# tensorflow在使用一个变量的同时要进行初始化操作
# 定义一个init初始化所有变量
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    print('减法流操作结果：',sess.run(sub))
    print('加法流操作结果：',sess.run(add))

'''
>>>法流操作结果： [-2 -1]
>>>加法流操作结果： [-1  1]
'''

# 定义一个变量，初始化为0，命名为counter（很多op都能进行命名操作）
state = tf.Variable(0, name='counter')
# 创建一个op，作用是使state加1
new_value = tf.add(state, 1)
# 幅值op，tensorflow的幅值不能直接通过等号进行，必须使用一个赋值函数tf.assign
update = tf.assign(state, new_value)
# 变量初始化
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    print(sess.run(state))
    for _ in range(5):
        sess.run(update)
        print('state变量的值：', sess.run(state))