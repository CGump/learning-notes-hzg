import tensorflow as tf
print("check tensorflow version: ", tf.__version__)
# tensorflow 创建图，启动图

# 创建一个常量op
m1 = tf.constant([[3,3]])
# 创建另一个常量op
m2 = tf.constant([[2],[3]])
# 创建一个矩阵乘法op，把m1、m2传入
product = tf.matmul(m1, m2)
# ！！！matmul是矩阵乘法、叉乘，multiply是数乘、点乘！！！
# 输出
print(product)
'''
到这步，只创建了图的op（tensor），并没有进行计算
>>>Tensor("MatMul:0", shape=(1, 1), dtype=int32)
'''
# 定义一个会话，启动默认图
sess = tf.Session()  # 定义sess使用tf.Session()类方法
# 调用sess的run方法来执行矩阵乘法op
# run(product)依次触发了图中3个op
result = sess.run(product)
print(result)
sess.close()

# 按上述可能比较麻烦，一般如下去定义
with tf.Session() as sess:
    # 调用sess的run方法来执行矩阵乘法op
    # run(product)依次触发了图中3个op
    result = sess.run(product)
    print(result)
    # 此时不需要再执行sess.close()操作，当会话执行完后自动关闭

