# python中的魔法函数

[toc]

## 0. 魔法函数大纲

1. 字符串表示

      * `__repr__`
      * `__str__`
2. 集合、序列相关

      * `__len__`
      * `__getitem__`
      * `__setitem__`
      * `__delitem__`
      * `__contains__`
2. 迭代相关

      * `__iter__`
      * `__next__`
3. 可调用

	  * `__call__`
4. with上下文管理器

      * `__enter__`
      * `__exit__`
5. 数值转换

      * `__abs__`
      * `__bool__`
      * `__int__`
      * `__float__`
      * `__hash__`
      * `__index__`
6. 元类相关

      * `__new__`
      * `__init__`
7. 属性相关

      * `__getattr__`、`__setatter__`
      * `__getattribute__`、`__setattribute__`
      * `__dir__`
9. 属性描述符
      * `__get__`、`__set__`、`__delete__`
10. 协程
      * `__awit__`
      * `__aiter__`
      * `__anext__`
      * `__aenter__`
      * `__aexit__`
11. 数学运算
       * 一元、二元、算术、反向算术、增量赋值算术运算、位运算、反向位运算、增量赋值位运算



## 1. 字符串表示

### `__str__`
> ```python
> def __repr__(self):
> ```

当使用print输出对象的时候，只要定义了`__str__(self)`方法，那么就会打印从在这个方法中`return`的数据，`__str__`方法需要返回一个字符串，当做这个对象的描写。

```python
class Company():
    def __init__(self, employee_list):
        self.employee = employee_list

    def __str__(self):
        return ",".join(self.employee)


if __name__ == '__main__':
    company = Company(["tom", "bob", "jane"])
    print(company)
    # 不构建时打印：<__main__.Company object at 0x000001E840D91A88>
    # 构建时打印：tom,bob,jane
```

有时候我们想让屏幕打印的结果不是对象的内存地址，而是它的值或者其他可以自定义的东西，以便更直观地显示对象内容，可以通过在该对象的类中创建或修改`__str__()`或`__repr__()`方法来实现（显示对应方法的返回值）
注意：`__str__()`方法和`__repr__()`方法的返回值只能是字符串！

**关于调用两种方法的时机**

- 使用`print()`时
- 使用`%s`和`{}.format`拼接对象时
- 使用`str(x)`转换对象x时

在上述三种场景中，会优先调用对象的`__str__()`方法；若没有，就调用`__repr__()`方法；若再没有，则显示其内存地址。

### `__repr__`

> ```python
> def __repr__(self):
> ```

默认情况下，`__repr__() `会返回和调用者有关的 “类名+object at+内存地址”信息。当然，我们可以通过在类中重写这个方法，从而实现当输出实例化对象时，输出我们想要的信息。相当于自我介绍。

```python
class Company():
    def __init__(self, employee_list):
        self.employee = employee_list

    def __repr__(self):
        return ",".join(self.employee)


if __name__ == '__main__':
    company = Company(["tom", "bob", "jane"])
    print(company)
```

特别地，对于下面两种场景：

- 用`%r`进行字符串拼接时
- 用`repr(x)`转换对象x时

则会调用这个对象的`__repr__()`方法；若没有，则**不再看**其是否有`__str__()`方法，而是显示其内存地址。

> ### 万能的`%r`
>
> `%r`是一个万能的格式付，它会将后面给的参数原样打印出来，带有类型信息。

## 8. 属性相关魔法函数

### `__setattr__`

> ```python
> def __setattr__(self, key, value)
> ```

会拦截所有属性的的赋值语句。如果定义了这个方法，`self.attr = value` 就会变成`self.__setattr__("attr", value)`.

这个需要注意。当在`__setattr__`方法内对属性进行赋值是，不可使用`self.attr = value`,因为他会再次调用`self.__setattr__("attr", value)`，则会形成无穷递归循环，最后导致堆栈溢出异常。应该通过对属性字典做索引运算来赋值任何实例属性，也就是使用`self.__dict__['name'] = value`.

```python
class A():
    def __init__(self):
        self.width = 3
        self.height = 4

    def __setattr__(self, key, value):
        print("add {} to class".format(key))
        self.__dict__[key] = value  # 如果没有则print(r.__dict__)为空

if __name__ == '__main__':
    r = A()
    r.size = (4,5)
    print(r.size)
    print(r.__dict__)
    
    """
    add width to class
    add height to class
    add size to class
    (4, 5)
    {'width': 3, 'height': 4, 'size': (4, 5)}
    """
```

### `__getattr__`

> ```python
> def __getattr__(self, item):
> ```

拦截点号运算。`对象.属性`：如果找不到属性，就会用属性名作为字符串，调用该方法；如果继承树可以找到该属性，则不会调用该方法。

```python
class A():
    def __init__(self):
        self.width = 3
        self.height =4
        self.size = (5, 6)

class B(A):
    def __getattr__(self, item):
        if item == "name":
            return "this is B"
        else:
            raise AttributeError("not this attribute {}".format(item))

if __name__ == '__main__':
    s = B()
    print(s.size)  # (5, 6)
    print(s.name)  # "this is B"
```

