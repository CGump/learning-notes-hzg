# Python列表推导式

列表解析式（List comprehension）或者称为列表推导式，是 Python 中非常强大和优雅的方法。它可以基于现有的列表做一些操作，从而快速创建新列表。在我们第一次见到列表推导式时，可能会感觉这种方法非常炫酷，因此写列表推导式是非常爽的一件事

## 什么是列表推导式

如果我们有一个列表，并希望抽取列表中的元素，那么最标准的方法是使用 Python 循环，但是我们也可以直接通过列表推导式，它只需一行代码就能搞定所有操作。当然，抽取列表元素的前提是，我们要理解列表是一种可迭代对象，它允许依次读取不同的元素。

想象一下，如果动物园中有很多不同的动物，每年每一只动物都需要定期体检，那么动物园就是列表。我们可以遍历整个动物园，并依次抽取动物，抽取的动物并不做进一步的处理，直接放到体检列表中。如下所示为一般 Python 循环的做法：

```python
# Creating our animal park
animal_park = ['Rabbit','Rabbit','Rabbit','Rabbit','Cat','Cat','Cat','Cat','Cat','Cat','Cat', 'Turtle','Turtle','Turtle','Turtle','Turtle','Turtle','Turtle', 'Dog','Dog', 'Kangaroo','Kangaroo','Kangaroo','Kangaroo','Kangaroo','Kangaroo']

# Creating a new list for our animal doctor with all animals
animal_doctor = []
for animal in animal_park:
   animal_doctor.append(animal)
```

上面的代码很简单，用一个 for 循环就行，它的语义也很容易理解。如下我们可以使用列表推导式重写这一个循环：
```py
animal_doctor = [animal for animal in animal_park]
```
通过列表推导式，我们将代码量由三行降低到一行。如果对比两者，我们会发现它们其实是一样的，差不多都是创建、遍历和接收三部分。

## 条件语句

这样看起来列表推导式也没什么大不了，但别忘了它还能对元素做进一步操作，例如加个条件语句。在标准的列表循环中，我们的条件语句如下所示会加到 for 循环中。
```py
animal_doctor = []
for animal in animal_park:
   if animal != 'Dog' and animal != 'Cat':
      animal_doctor.append(animal)
```
在列表推导式中，我们可以将条件加到里面，用稍微长一点的单行代码完成整个流程。上面代码块可以等价地表达为：
```py
animal_doctor = [animal for animal in animal_park if animal != 'Dog' and animal != 'Cat']
```

另外非常重要的一点是，列表推导式的速度非常快。如下两者都加了条件语句，但是列表推导式要比一般的循环语句快了 51%。

最后，如果你使用过列表推导式创建新的列表，那么你最好一直使用它，因为我们没有原因再使用标准 Python 循环。我们可以发现，只要明晰了基本概念，那么列表推导式还是非常容易使用的。
