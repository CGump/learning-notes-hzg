# easydict库
easydict的作用：可以使得以属性的方式去访问字典的值！
```
>>> from easydict import EasyDict as edict
>>> d = edict({'foo':3, 'bar':{'x':1, 'y':2}})
>>> d.foo
3
>>> d.bar.x
1
 
>>> d = edict(foo=3)
>>> d.foo
3
```

也可以这样用，以属性的方式进行赋值！
```
>>> d = EasyDict()
>>> d.foo = 3
>>> d.foo
3
```
```
>>> d = EasyDict(log=False)
>>> d.debug = True
>>> d.items()
[('debug', True), ('log', False)]
```
```
>>> class Flower(EasyDict):
...     power = 1
...
>>> f = Flower({'height': 12})
>>> f.power
1
>>> f['power']
1
```