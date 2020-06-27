# Python--lambda表达式


lambda表达式，通常是在需要一个函数，但是又不想费神去命名一个函数的场合下使用，也就是指匿名函数。

lambda所表示的匿名函数的内容应该是很简单的，如果复杂的话，干脆就重新定义一个函数了，使用lambda就有点过于执拗了。

lambda就是用来定义一个匿名函数的，如果还要给他绑定一个名字的话，就会显得有点画蛇添足，通常是直接使用lambda函数。如下所示：
```
add = lambda x, y : x+y
add(1,2)  # 结果为3
```
那么到底要如何使用lambda表达式呢？

 

## 1、应用在函数式编程中

Python提供了很多函数式编程的特性，如：map、reduce、filter、sorted等这些函数都支持函数作为参数，lambda函数就可以应用在函数式编程中。如下：

*需求：将列表中的元素按照绝对值大小进行升序排列*
```
list1 = [3,5,-4,-1,0,-2,-6]
sorted(list1, key=lambda x: abs(x))
```
当然，也可以如下：
```
list1 = [3,5,-4,-1,0,-2,-6]
def get_abs(x):
    return abs(x)
sorted(list1,key=get_abs)
```
只不过这种方式的代码看起来不够Pythonic

 

## 2、应用在闭包中
```
def get_y(a,b):
     return lambda x:ax+b
y1 = get_y(1,1)
y1(1) # 结果为2
```
当然，也可以用常规函数实现闭包，如下：
```
def get_y(a,b):
    def func(x):
        return ax+b
    return func
y1 = get_y(1,1)
y1(1) # 结果为2
```
只不过这种方式显得有点啰嗦。

那么是不是任何情况下lambda函数都要比常规函数更清晰明了呢？肯定不是。

Python之禅中有这么一句话：Explicit is better than implicit（明了胜于晦涩），就是说那种方式更清晰就用哪一种方式，不要盲目的都使用lambda表达式。

## 3、yolo中的lambda函数

> ```python
> use_lambda = reduce(lambda f, g: lambda *a, **kw: g(f(*a, **kw)), funcs)  # funcs是来自输入的*funcs，是一个元组
> ```

首先这里采用了`reduce()`函数，该函数会将`funcs`中的元素一一输入至第一项的lamba函数进行运算。

比如定义相加函数

```python
def add(x, y):
    return x+y

ans = reduce(add, [1,2,3,4])
print(ans)  # 10
```

首先reduce会将列表中的1、2作为输入给到add（1，2）函数计算返回3，此时返回值再和列表中的第三个元素3输入至add（3，3）返回6，再与第四元素4作为输入add（6，4）计算得出10，所以它的逻辑调用为：add（add（add（1，2），3），4）。

下面是lambda函数块：

首先为了理解方便，这里定义了一个参数use_lambda将后面的语句进行赋值，由于语句中输入的是函数，因此use_lambda也是函数对象，

首先是第一个lambda，他的输入参数是（f，g），他的内容位于：后面

接着在第二个lambda，他的输入是（*a，**kw），该输入会捕捉调用use_lambda（）时的输入参数，

然后是第二个lambda的内容：g（f（*a，**kw）），该内容是对第一个lambda输入函数f、g的调用，

因此整个lambda模块可以写成：

```python
def func1(f, g):
    def func2(*a, **kw):
        return g(f(*a, **kw))
    return func2
```

最终返回的是func2的引用，

接下来就是处理reduce函数的任务，首先我们假定以下函数：

```python
def add(x):
    return x + 5


def mut(x):
    return x ** 2

# 这里a变量存放着函数的引用，可以看成是一个函数的函数名
a = reduce(lambda f, g: lambda *args, **kwargs: g(f(*args, **kwargs)), [add, mut, add]) 
print(a(1))
# 41
```

首先f = add，g = mut，lambda函数输出f（g（*args，**kwargs））的引用，

然后再将引用与最后一个add作为输入，输入进lambda函数，此时新的 f =mut（add（*args，**kwargs）），g=add，

输入出就变为add（mut（add（*args，**kwargs））（\*args，\*\*kwargs）），简化一下就是：

add（mut（add（*args，**kwargs））），输出的依然是函数的引用。

因此最后在调用a（1）的时候，此时给到了具体的值，完成add（mut（add（*args，**kwargs）））（1）的计算，即为

add（mut（add（1）））= （（1+5）**2）+5 = 41

