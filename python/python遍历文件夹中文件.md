# python遍历文件夹中所有文件
遍历文件需要用到python的os库，`path`为指定的目录
* 通过`os.listdir()`函数获取`path`路径下的所有文件列表
* 通过`enumerate()`函数进行排序和抽取，其结果为`序号, 名称`
* 最后通过`for`循环控制进行遍历

```
import os
for i,pic_name in enumerate(os.listdir(path)):
    name = pic_name.split('.')[0]
```