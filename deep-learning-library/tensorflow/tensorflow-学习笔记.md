# tensorflow学习笔记

函数API与具体使用教程参考：[tensorflow中文文档](http://www.tensorfly.cn/tfdoc/get_started/introduction.html)

---
## 几点说明
* tensorflow在构建时只是进行了数据流图的构建，实际计算还需要调用`Session()`类中的`run()`方法
* 要查看单个或多个op参数的值，需要将所定义的op点以列表的形式放入`run()`中进行Fetch操作，并按顺序取出，例如：
`see_prediction, see_loss, see_arg = sess.run([prediction, loss, arg])`
* 训练时数据可以通过预先定义的占位符进行实时输入，必须通过`feed_dict=`参数以字典的格式进行一一对应，例如：
`sess.run(train_step, feed_dict={x:batch_xs, y:batch_ys})`


---
## `tf.nn.softmax()`函数
softmax()函数，或称归一化指数函数，是逻辑函数的一种推广。它能将一个含任意实数的K维向量“压缩”到另一个K维实向量中，使得每一个元素的范围都在之间，并且所有元素的和为1。
$$ \sigma(z)_j = \frac {e^{z_j}}{\sum_{k=1}^Ke^{z_k}}  $$

```
>>>a = [[1.0, 2.0, 6.0],
        [2.0, 9.0, 15.0]]

>>>tf.nn.softmax(a)

>>>[[6.5732626e-03 1.7867981e-02 9.7555870e-01]
    [2.2547354e-06 2.4726177e-03 9.9752516e-01]]
```
比如`a = [1.0, 2.0, 6.0]`，softmax函数计算$[\frac{e^1}{e^1+e^2+e^6} , \frac{e^2}{e^1+e^2+e^6} , \frac{e^6}{e^1+e^2+e^6}]$，最后得到`[6.5732626e-03 1.7867981e-02 9.7555870e-01]`

由此可以看出softmax通过指数的形式对一个集合的数进行变换，把较小值的变得更小，较大值的变得更大，容易进行区分和筛选。

---
## `tf.argmax()`函数

在计算识别准确率的经常用到`tf.argmax()`函数，其作用是提取预测结果中准确率（概率）最大的元素在该维度的位置例如
```
import tensorflow as tf
print("check tensorflow version: ", tf.__version__)

a = [[0.15, 0.80, 0.05],[0.04, 0.36, 0.60]]

with tf.Session() as sess:
    print(sess.run(tf.argmax(a, demension=1)))

>>>[1 2]
```
其中`demension`控制输入tensor的维度，`demension=1`时为按行索引，其结果为第1行第1个，第2行第2个：0.80、0.60

---
## batch_size 与 loss 和梯度下降速率的关系，以及对准确率计算的影响
由于loss的计算和梯度下降速率的更新是在计算一个batch_size时进行，而每个epoch的准确率计算则是整体数据完成一个epoch中所有batch后才进行。因此batch_size在训练的时候如果设置过大，数据总量不变的情况下，一个epoch计算的batch量少，梯度更新的次数少，loss的下降速度就会很慢。很直观的特点就是导致训练的准确率在一定的epoch内保持在一个较低的值中不会变化。


mnist数据训练练习时，以下是在batch_size设置在8时的训练准确率情况，可以看到每个epoch的变化速度很快，loss下降的速度很快，准确率提升的速度在20个epoch完成后提高了0.5左右。
```
batch_size = 8
Iter 0. Testing Accuracy 0.1135
Iter 1. Testing Accuracy 0.208
Iter 2. Testing Accuracy 0.244
Iter 3. Testing Accuracy 0.2563
Iter 4. Testing Accuracy 0.2718
Iter 5. Testing Accuracy 0.2817
Iter 6. Testing Accuracy 0.2897
Iter 7. Testing Accuracy 0.2918
Iter 8. Testing Accuracy 0.3153
Iter 9. Testing Accuracy 0.3419
Iter 10. Testing Accuracy 0.3557
Iter 11. Testing Accuracy 0.38
Iter 12. Testing Accuracy 0.3791
Iter 13. Testing Accuracy 0.395
Iter 14. Testing Accuracy 0.3955
Iter 15. Testing Accuracy 0.455
Iter 16. Testing Accuracy 0.4837
Iter 17. Testing Accuracy 0.523
Iter 18. Testing Accuracy 0.5478
Iter 19. Testing Accuracy 0.5724
Iter 20. Testing Accuracy 0.5982
```
而把batch_size设置为100后，在第14个epoch前训练准确率始终保持在0.1135不变，直到第20个epoch时训练准确率也只上升了0.1.
```
batch_size = 100
Iter 0. Testing Accuracy 0.1135
Iter 1. Testing Accuracy 0.1135
Iter 2. Testing Accuracy 0.1135
Iter 3. Testing Accuracy 0.1135
Iter 4. Testing Accuracy 0.1135
Iter 5. Testing Accuracy 0.1135
Iter 6. Testing Accuracy 0.1135
Iter 7. Testing Accuracy 0.1135
Iter 8. Testing Accuracy 0.1135
Iter 9. Testing Accuracy 0.1135
Iter 10. Testing Accuracy 0.1135
Iter 11. Testing Accuracy 0.1135
Iter 12. Testing Accuracy 0.1135
Iter 13. Testing Accuracy 0.1135
Iter 14. Testing Accuracy 0.114
Iter 15. Testing Accuracy 0.1229
Iter 16. Testing Accuracy 0.1621
Iter 17. Testing Accuracy 0.1889
Iter 18. Testing Accuracy 0.2017
Iter 19. Testing Accuracy 0.2073
Iter 20. Testing Accuracy 0.2113
```
---