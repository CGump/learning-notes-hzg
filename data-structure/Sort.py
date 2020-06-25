# -*- coding: utf-8 -*-
# ================================================================
#
#   Editor      : PyCharm
#   File name   : Sort.py
#   Author      : CGump
#   Email       : huangzhigang93@qq.com
#   Created date: 2020/6/25 22:46
#
# ================================================================


def selection_sort(inputs: list):
    for i in range(0, len(inputs)-1):
        minimum = i
        for j in range(i+1, len(inputs)):
            if inputs[j] < inputs[minimum]:
                minimum = j
        inputs[i], inputs[minimum] = inputs[minimum], inputs[i]
    return inputs


def quick_sort(inputs: list):
    if len(inputs) < 2:
        return inputs
    keys = inputs.pop(0)
    less = []
    greater = []
    for item in inputs:
        if item < keys:
            less.append(item)
        else:
            greater.append(item)
    return quick_sort(less) + [keys] + quick_sort(greater)


def bubble_sort(inputs: list):
    lengths = len(inputs)
    while lengths > 0:
        for i in range(0, len(inputs)-1):
            if inputs[i] > inputs[i+1]:
                inputs[i], inputs[i+1] = inputs[i+1], inputs[i]
        lengths -= 1
    return inputs


if __name__ == '__main__':
    rst = quick_sort([3, 5, 1, 2, 4])
    print(rst)
    rst = bubble_sort([3, 5, 1, 2, 4])
    print(rst)
    rst = selection_sort([3, 5, 1, 2, 4])
    print(rst)
