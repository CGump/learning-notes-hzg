# python中yield和return的区别

* return是用来返回具体的某个值
* yield一般与循环一起用，相当于生成了一个容器(常见的就是字典)，然后在这个容器里面存放了每次循环以后的值，并且就在那放着，不输出，不返回，等你下次需要他的时候直接取出来用(调用)就行

函数在执行到return的时候就停止，而遇到yield时能够持续不中断地获取函数的每个输出值。这一点很像labview中循环的通道，可以每循环一次输出一个值。

return的案例：
```
def test():
    for i in range(5):
        return i

if __name__ == "__main__":
    print(test())

>>>0
```
yield的案例：
```
def yield_test():
    for i in range(5):
        yield call(i)  # 它会立即把call(i)输出，在main中的for循环中把值传递给n，
                       # 所以print("main loop n =", n, "in yield back")会先执行
        print("yield_test loop i =", i) #后执行

    print("do something")  # 待执行，循环完成后执行一次
    print("end.")

def call(i):  
    return i*2  

if __name__ == "__main__":
    for n in yield_test():
        print("main loop n =", n, "in yield_test() back")

>>> main loop n = 0 in yield_test() back
    yield_test loop i = 0
    main loop n = 2 in yield_test() back
    yield_test loop i = 1
    main loop n = 4 in yield_test() back
    yield_test loop i = 2
    main loop n = 6 in yield_test() back
    yield_test loop i = 3
    main loop n = 8 in yield_test() back
    yield_test loop i = 4
    do something
    end.
```

> **理解的关键在于：下次迭代时，代码从yield的下一跳语句开始执行.**  

举一个简单的例子，定义一个迭代器generator，依次返回数字1，3，6：
```
def odd():
    print('step 1')
    yield 1
    print('step 2')
    yield 3
    print('step 3')
    yield(6)  # 也可以用括号进行给定值 
```
调用该迭代器时，首先要生成一个generator的对象，然后用next()函数不断获得下一个返回值：
```
>>> o=odd()
>>> next(o)
step 1
1
>>> next(o)
step 2
3
>>> next(o)
step 3
6
>>> next(o)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

可以看到，odd不是普通函数，而是generator，在执行过程中，遇到yield就中断，下次又继续执行。执行3次yield后，已经没有yield可以执行了，所以，第4次调用next(o)就报错。