# 定义一个队列
class MyQueue(object):
    def __init__(self, size):
        # 定义初始化队列长度
        self.size = size  # 定义队列长度
        self.queue = []  # 存储队列，以列表的形式进行队列操作

    def __str__(self):
        # 返回对象的字符串表达式，方便查看
        return str(self.queue)

    def isEmpty(self):
        # 判断队列是否为空
        if len(self.queue) == 0:
            return True
        return False
    
    def isFull(self):
        # 判断队列是否为满
        if len(self.queue) == self.size:
            return True
        return False
    
    def inQueue(self, n):
        # 入队
        if self.isFull():
            return -1
        self.queue.append(n)  # 列表末尾添加新的对象
    
    def outQueue(self):
        # 出队
        if self.isEmpty():
            return -1
        firstelement = self.queue[0]  # 提取队头元素
        self.queue.remove(firstelement)  # 删除队头操作
        return firstelement
    
    def delete(self, n):
        # 删除某元素
        element = self.queue[n]
        self.queue.remove(element)
    
    def clear(self):
        # 删除队列，该队列就不存在了
        del self.queue
    
    def getSize(self):
        # 获取当前长度
        return len(self.queue)

    def getnumber(self, n):
        # 获取某个元素
        element = self.queue[n]
        return element

if __name__ == "__main__":
    queue = MyQueue(5)
    for i in range(8):
        # 先判断队列是否为满
        if not queue.isFull():
            queue.inQueue(i)
        else:
            # 为满时则先出队再入队
            queue.outQueue()
            queue.inQueue(i)
        print(queue)