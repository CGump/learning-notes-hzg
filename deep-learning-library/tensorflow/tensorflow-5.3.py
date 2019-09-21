import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.contrib.tensorboard.plugins import projector
print("check tensorflow version: ", tf.__version__)
# tensorflow tensorboard 训练可视化
# 每运行一次需要把前一次logs文件夹中的tensorboard缓存删除

# 载入数据集
mnist = input_data.read_data_sets("MNIST_data", one_hot=True)
# 运行次数
max_steps = 1001
# 图片数量
image_num = 3000
# 文件路径
DIR = 'F:/learning-notes-hzg/deep-learning-library/tensorflow/'

# 定义会话
sess = tf.Session()

# 载入图片
embedding = tf.Variable(tf.stack(mnist.test.images[:image_num]), trainable=False, name='embedding')

# 定义一个分析函数
def variable_summarie(var):
    with tf.name_scope('summaries'): # 大命名空间，计算一系列的参数
        mean = tf.reduce_mean(var)  # 计算参数平均值
        tf.summary.scalar('mean', mean) # 给计算的参数命名为平均值
        with tf.name_scope('stddev'):  #小命名空间，计算标准差
            stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean))) # 计算标准差
        tf.summary.scalar('stddev', stddev) # 命名为标准差
        tf.summary.scalar('max', tf.reduce_max(var)) # 计算并命名为最大值
        tf.summary.scalar('min', tf.reduce_min(var)) # 计算并命名为最小值
        tf.summary.histogram('histogram', var) # 统计直方图

# 命名空间
with tf.name_scope('input'):
    # 这里none表示第一个维度可以是任意的长度
    x = tf.placeholder(tf.float32, [None, 784], name='x-input')
    # 正确的标签
    y = tf.placeholder(tf.float32, [None, 10], name='y-input')

# reshape图片
with tf.name_scope('input_reshape'):
    image_shaped_input = tf.reshape(x, [-1, 28, 28, 1]) # -1代表一个不确定的值，任意值，后面的1是维度，因为用的是黑白的所以是1
    tf.summary.image('input', image_shaped_input, 10)

with tf.name_scope('layer'):
    # 创建一个简单的神经网络
    with tf.name_scope('wights'):
        W = tf.Variable(tf.zeros([784, 10]), name='W')
        variable_summarie(W) 
    with tf.name_scope('biases'):
        b = tf.Variable(tf.zeros([10]), name='b')
        variable_summarie(b) 
    with tf.name_scope('wx_plus_b'):
        wx_plus_b = tf.matmul(x, W) + b
    with tf.name_scope('softmax'):
        prediction = tf.nn.softmax(wx_plus_b)

with tf.name_scope('loss'):
    # 交叉熵代价函数
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=prediction))
    tf.summary.scalar('loss', loss)
with tf.name_scope('train'):
    # 梯度下降法
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(loss)

# 初始化变量
sess.run(tf.global_variables_initializer())

with tf.name_scope('accuracy'):
    with tf.name_scope('correct_prediction'):
        # 结果存放在一个布尔型变量中
        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(prediction, 1)) # argmax返回一维张量中最大值所在的位置
    with tf.name_scope('accuracy'):
        # 求准确率
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32)) # 把correct_prediction变成float32类型
        tf.summary.scalar('accuracy', accuracy)

# 产生metadata文件
if tf.gfile.Exists(DIR + 'projector/projector/metadata.tsv'):
    tf.gfile.DeleteRecursively(DIR + 'projector/projector/metadata.tsv')
with open(DIR + 'projector/projector/metadata.tsv', 'w') as f:
    labels = sess.run(tf.argmax(mnist.test.labels[:], 1))
    for i in range(image_num):
        f.write(str(labels[i]) + '\n')

# 合并所有的summary
merged = tf.summary.merge_all()

projector_writer = tf.summary.FileWriter(DIR + 'projector/projector', sess.graph)
saver = tf.train.Saver()
config = projector.ProjectorConfig()
embed = config.embeddings.add()
embed.tensor_name = embedding.name
embed.metadata_path = DIR + 'projector/projector/metadata.tsv'
embed.sprite.image_path = DIR + 'projector/data/mnist_10k_sprite.png'
embed.sprite.single_image_dim.extend([28, 28])
projector.visualize_embeddings(projector_writer, config)

for i in range(max_steps):
    # 每个批次100个样本
    batch_xs, batch_ys = mnist.train.next_batch(100)
    run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
    run_metadata = tf.RunMetadata()
    summary,_ = sess.run([merged, train_step], feed_dict={x:batch_xs, y:batch_ys}, options=run_options, run_metadata=run_metadata)
    projector_writer.add_run_metadata(run_metadata, 'step%03d' % i)
    projector_writer.add_summary(summary, i)

    if i%100 == 0:
        acc = sess.run(accuracy, feed_dict={x:mnist.test.images, y:mnist.test.labels})
        print("Iter" + str(i) + ", Testing Accuracy= " + str(acc))

saver.save(sess, DIR + 'projector/projector/a_model.ckpt', global_step=max_steps)
projector_writer.close()
sess.close()
