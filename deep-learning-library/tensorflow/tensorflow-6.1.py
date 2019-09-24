import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
print("check tensorflow version: ", tf.__version__)
# tensorflow 卷积神经网络

mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

# 每个批次大小
batch_size = 100
# 一共计算的批次数 总数/批次大小
n_batch = mnist.train.num_examples // batch_size

# 初始化权值
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1) # 生成一个截断的正态分布
    return tf.Variable(initial)

# 初始化偏置
def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

# 卷积层
def conv2d(x, W):
    '''
    x input tensor of shape '[batch, in_height, in_width, in_channels]'
    W filter / kernel tensor of shape `[filter_height, filter_width, in_channels, out_channels]`
    `strides[0] = strides[3] = 1`, strides[1]代表x方向的步长，strides[2]代表y方向的步长
    padding: A `string` from: `"SAME", "VALID"`.
    '''
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

# 池化层
def max_pool_2x2(x):
    # ksize [1,x,y,1]
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

# 定义两个placeholder
x = tf.placeholder(tf.float32, [None, 784]) # 28*28=784
y = tf.placeholder(tf.float32, [None, 10])
keep_prob = tf.placeholder(tf.float32)

# 改变x的格式转换为4D向量`[batch, in_height, in_width, in_channels]`
x_image = tf.reshape(x, [-1, 28, 28, 1])

# 初始化第一个卷积层的权值和偏重
W_conv1 = weight_variable([5, 5, 1, 32])  # 5*5的采样窗口，32个卷积核从1个平面（通道）抽取特征
b_conv1 = bias_variable([32])  # 每个卷积核一个偏置值

# 把x_image和权值向量进行卷积，再加上偏置，然后应用于relu激活函数
# 28*28*1 的图片卷积之后变为28*28*32
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
# 池化之后变为 14*14*32
h_pool1 = max_pool_2x2(h_conv1) # 进行max-pooling

# 初始化第二个卷积层的权值和偏置
# 第二次卷积之后变为 14*14*64
W_conv2 = weight_variable([5, 5, 32, 64]) # 5*5的采样窗口，64个卷积核从32个平面抽取特征
b_conv2 = bias_variable([64]) # 每一个卷积核一个偏置值
# 把第一层卷积的输出h_pool1和权值向量进行卷积，再加上偏置，然后应用于relu激活函数
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
# 第二次池化之后变为 7*7*64
h_pool2 = max_pool_2x2(h_conv2)

# 28*28的图片在两次卷积和池化后变为7*7*64的平面

# 第一个全连接层
W_fc1 = weight_variable([7*7*64, 1024])
b_fc1 = bias_variable([1024])
# 7*7*64的图像变成1维向量
h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64]) # 这里把第二层池化的输出进行了扁平化，才可以适配全连接层的参数
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

# 第二个全连接层
W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])
logits = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
prediction = tf.nn.sigmoid(logits)

loss = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=logits))
train_step = tf.train.AdamOptimizer(0.001).minimize(loss)

prediction_2 = tf.nn.softmax(prediction)
correct_prediction = (tf.equal(tf.argmax(prediction_2, 1), tf.argmax(y, 1)))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for epoch in range(21):
        for batch in range(n_batch):
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            sess.run(train_step, feed_dict={
                     x: batch_xs, y: batch_ys, keep_prob: 0.7})
        acc = sess.run(accuracy, feed_dict={
                       x: mnist.test.images, y: mnist.test.labels, keep_prob: 1.0})
        print("Iter: " + str(epoch) + ", acc: " + str(acc))
