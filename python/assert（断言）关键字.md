# python 断言 assert 关键字
Python assert（断言）用于判断一个表达式，在表达式条件为 false 的时候触发异常。通常用于异常处理。也可以通过要判断的表达式后面紧跟一串字符串，来解释发生异常的原因。

以下为assert使用实例：
```python
>>> assert True     # 条件为 true 正常执行
>>> assert False    # 条件为 false 触发异常
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AssertionError
>>> assert 1==1    # 条件为 true 正常执行
>>> assert 1==2    # 条件为 false 触发异常
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AssertionError

>>> assert 1==2, '1 不等于 2'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AssertionError: 1 不等于 2
```