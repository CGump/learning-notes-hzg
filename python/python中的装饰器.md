# 一些常用装饰器的使用方法

[toc]

## 0. 写在前面：闭包函数与装饰器

### 什么是闭包函数

**闭包的特点就是内部函数引用了外部函数中的变量。** 在Python中，支持将函数当做对象使用，也就是可以将一个函数当做普通变量一样用作另一个函数的参数和返回值。拥有此类特性的语言，一般都支持闭包。

闭包内函数引用外函数内部的变量，不会因为外部函数的结束而释放掉，而是一直保存在内存中直到内部函数被调用完成后销毁。

```python
def func():
    name = 'python'
    def inner():
        print(name)
    return inner

f = func()  # f = func() = inner 
f()  # f() = inner 
```

### 为什么闭包函数能捕捉到外部输入

闭包函数在进行调用时，外部函数返回的是内部函数的函数名，因此在调用结束后使用该函数时，所给到的参数就直接被闭包的内函数捕捉。这点是实现装饰器原理的最重要原因。

```python
def func1():
    def func2(x):
        print(x ** 2)
    return func2

# 调用func1
use = func1()
# 此时ues指向的是func2的引用，因此在调用use时，use的函数输入3就给到了func2的输入参数x，从而完成捕捉
use(3)
```

### 什么是装饰器（decorator）

**装饰器，就是增强函数或类的功能的一个函数。**

假如定义一个add函数，

```python
def add(a, b):
    result = a + b
    return result
```

需要计算add函数的执行时间，这时可以这样写：

```python
import time

def add(a, b):
    start_time = time.time()
    result = a + b
    end_time = time.time() - start_time
    print("函数的计算花费时间为：", end_time)
    return result  
```

但如果要同样的方法去计算一个乘法函数的计算时间呢？那还需要在函数内再写一遍。每个代码都需要改动一遍。因此可以引入装饰器：

```python
import time

def time_calc(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time() - start_time
        print("函数的计算时间是：", end_time)
        return res
    return wrapper

@time_calc
def add(a, b):
    result = a + b
    return result

add(3, 5)
# 函数的计算时间是： 0.0
```

使用装饰器后简化了调用过程，在不使用装饰器的情况下，上面`add(3, 5)`的调用逻辑应该为：`time_calc(add)(3, 5)`。

因此一个装饰器的主要构成有：

```python
def decorator(func):  # <- 以函数名作为输入
    def wrapper(*args, **kwargs):  # <- 内部函数定义装饰器函数逻辑
        # 装饰器函数内部逻辑
        # 装饰器函数内部逻辑
        return func(*args, **kwargs)  # <- 内部函数返回输入函数的调用
    return wrapper  # <- 外部函数返回内部函数的函数名
```



## 1.  类方法装饰器`@property`

首先，再python中@property的定义是一个装饰器类，而不是一个装饰器函数。

`@property`装饰器可以让类中的方法以属性的方式进行调用,例如:
我们新建一个`Student()`类,并创建实例属性`_score`:


```python
class Student(object):
    def __init__(self):
        self._score = 70
    
    def get_score(self):
        return self._score
    
    def set_score(self, value):
        if not isinstance(value, int):
            raise ValueError("score must be an integer!")
        if value<0 or value>100:
            raise ValuError("score must between 0~100!")
        self._score = value

s = Student()
```


```python
s._score
70
```

此时,如果我们需要拿到或更改类中的示例属性`self._name`,则必须通过严格的调用类中`get_score`和`set_score`的方法:


```python
print(s.get_score())
s.set_score(80)
print(s.get_score())
```

    70
    80


上面的方法略显复杂,如果需要更改`_score`属性的话需要先执行`set_score`更改,没有直接用属性那么方便.但是,如果直接用属性进行设置,由无法检查参数.

所以,此时我们可以通过使用`@property`装饰器,对`get_score`和`set_score`进行改装,使类中的这两种方法变成类的属性,使得调用的时候可以以属性的方法进行.


```python
class Student(object):
    def __init__(self):
        self._score = 70
    
    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError("score must be an integer!")
        if value<0 or value>100:
            raise ValuError("score must between 0~100!")
        self._score = value

s = Student()
```

值得一提的是,`@property`装饰器自带`getter`和`setter`方法,分别用于将一个getter方法和一个setter方法变为属性,直接以`@property`装饰时默认为`getter`.


```python
print(s.score)
s.score = 80
print(s.score)
```

    70
    80


这样我们就发现,通过属性的方式调用,代码更加简洁易懂,同时又免去了方法调用的().

更重要的是,直接调用`score`即可，而不用知道属性名`_score`，因此用户无法更改属性，从而保护了类的属性。

## 2. 函数装饰器@wraps

Python装饰器在实现的时候，被装饰后的函数其实已经是另外一个函数了（函数名等函数属性会发生改变），为了不影响，Python的functools包中提供了一个叫wraps的decorator来消除这样的副作用。写一个decorator的时候，最好在实现之前加上functools的wrap，它能保留原有函数的名称和docstring。这里的docstring表示的是函数的第一段注释。

```python
from functools import wraps

def my_decorator(func):
    def wrapper(*args, **kwargs):
        '''this is wrapper'''
        print('Calling decorated function...')
        return func(*args, **kwargs)
    return wrapper  
 
@my_decorator 
def example():
    """this is example""" 
    print('Called example function')
    
print(example.__name__, example.__doc__)
example()
```

```
name:wrapper, doc:this is wrapper
Calling decorated function...
Called example function
```

加入@wraps装饰器之后

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """this is wrapper"""
        print('Calling decorated function...')
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def example():
    """this is example"""
    print('Called example function')
    
print("name:{}, doc:{}".format(example.__name__, example.__doc__))
example()
```

```
name:example, doc:this is example
Calling decorated function...
Called example function
```

还有的情况下，可以直接对函数进行装饰，比如说如下定义了卷积函数`Conv2D()`，和自定义的卷积函数`DarknetConv2D()`，使用装饰器`@wraps`可以使得两者的`__name__` 和`__doc__ `保持一致。

```python
from functools import wraps

def Conv2D(inputs):
    """this is Conv2D"""
    print("Conv2D的输入是：", inputs)

@wraps(Conv2D)
def Darknet2D(inputs):
    """this is Darknet2D"""
    print("Darknet2D的输入是：", inputs)

print("name:{}, doc:{}".format(Darknet2D.__name__, Darknet2D.__doc__))
Darknet2D(90)
```

```
name:Conv2D, doc:this is Conv2D
Darknet2D的输入是： 90
```



