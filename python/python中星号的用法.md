# Python中*和**的区别

Python中，（*）会把接收到的参数形成一个元组，而（**）则会把接收到的参数存入一个字典

我们可以看到，`foo`方法可以接收任意长度的参数，并把它们存入一个元组中
```
>>> def foo(*args):
...     print(args)
...
>>> foo("fruit", "animal", "human")
('fruit', 'animal', 'human')
>>> foo(1, 2, 3, 4, 5)
(1, 2, 3, 4, 5)
>>> arr = [1, 2, 3, 4, 5]  # 如果我们希望将一个数组形成元组，需要在传入参数的前面 加上一个*
>>> foo(arr)
([1, 2, 3, 4, 5],)
>>> foo(*arr)
(1, 2, 3, 4, 5)
```
（**）将接收到的参数存入一个字典
```	
>>> def foo(**kwargs):
...     for key, value in kwargs.items():
...         print("%s=%s" % (key, value))
...
>>> foo(a=1, b=2, c=3)
a=1
b=2
c=3
```
　

（*）和（**）一起使用　
```	
>>> def foo(*args, **kwargs):
...     print("args:", args)
...     print("kwargs:", kwargs)
...
>>> foo(1, 2, 3, a=1, b=2)
args: (1, 2, 3)
kwargs: {'a': 1, 'b': 2}
>>> arr = [1, 2, 3]
>>> foo(*arr, a=1, b=2)
args: (1, 2, 3)
kwargs: {'a': 1, 'b': 2}
```
　　

`name`作为`foo`第一个参数，在调用`foo("hello", 1, 2, 3, middle="world", a=1, b=2, c=3)`方法时，自然而然捕获了"hello"，而`middle`必须经过指定关键字参数才可以捕获值，否则会和之前的参数一样形成一个元组
```	
>>> def foo(name, *args, middle=None, **kwargs):
...     print("name:", name)
...     print("args:", args)
...     print("middle:", middle)
...     print("kwargs:", kwargs)
...
>>> foo("hello", 1, 2, 3, a=1, b=2, c=3)
name: hello
args: (1, 2, 3)
middle: None
kwargs: {'a': 1, 'b': 2, 'c': 3}
>>> foo("hello", 1, 2, 3, middle="world", a=1, b=2, c=3)
name: hello
args: (1, 2, 3)
middle: world
kwargs: {'a': 1, 'b': 2, 'c': 3}
>>> my_foo = {"name": "hello", "middle": "world", "a": "1", "b": "2", "c": "3"}
>>> foo(**my_foo)
name: hello
args: ()
middle: world
kwargs: {'a': '1', 'b': '2', 'c': '3'}
```
　　

此外，我们还可以定义一个字典`my_foo`，并以`foo(**my_foo)`这样的方式，让`name`和`middle`各自捕获自己的值，没有捕获的则存入一个字典

 

当我们删除`my_foo`中的`name`，再像之前传入函数，函数会报错说需要`name`这个参数
```	
>>> del my_foo["name"]
>>> foo(**my_foo)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: foo() missing 1 required positional argument: 'name'
```