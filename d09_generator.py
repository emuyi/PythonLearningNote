# todo iterable、iterator、generator

"""
1、为什么所有的序列的都是可迭代的？
    这牵涉到 python 处理序列迭代的机制：
        1、当序列内部实现 __iter__ 方法时，会返回一个迭代器对象，python 可以直接进行迭代
        2、当序列内部没有实现 __iter___ 方法，实现了__getitem__ 方法，python 内部会创建一个迭代器，然后从 索引0
          开始对序列进行迭代处理。
    几乎所有的序列实现的都有 __getitem___ 方法，所以python的序列都是可迭代的。

2、标准的python序列对象除了 __getitem__ 方法，内部也实现了 __iter__ 方法，这其实时一种比较极端的鸭子类型。
   正常来讲，如何判定一个对象是否时可迭代对象，只需看起内部是否实现了 __iter__ 方法就可以。但 python 的序列是一种
   例外，这也就说明了一个问题。不能单纯的去使用 isinstance(x, abc.Iterable) 去判定一个对象是否是可迭代对象，
   因为对于不标准的序列，这个测试无法通过，应该通过try/except 去处理。

3、迭代器：对象内部实现了__next__ 和 __iter__ （往往返回 self 就可以） 方法，使用 next() 可以获取迭代器中的元素，当迭代器中没有元素的时候，
   抛出 StopIteration 的异常。检测一个对象是否是迭代器，可以使用 isinstance(x, abc.Iterator)

4、可迭代对象和迭代器的关系？
    python 从可迭代对象中获取迭代器。即 iter(iterable) 变成一个迭代器。
    ”for 循环/ 列表推导/ 元组拆包 其实都是把可迭代对象变成了迭代器，并捕获了 StopIteration 的异常“

5、生成器函数
    含有 yield 关键字的函数就是生成器函数，yield 关键字一是生成器函数的标志，二用来生成值
    生成函数本质上来讲是一个生成器工厂函数，直接调用返回的是生成器对象，取值则是使用next()
    生成器函数中可以有return关键字，主要就是用来退出生成器函数触发 StopIteration 异常【常用在协程中】

6、生成器内部实现了迭代器的接口，所以生成器本质上来讲是一种迭代器。
7、惰性运算和急切运算 re.finditer/re.findall；生成器表达式/列表推导式
    如：
    def gen_func():
        print('start')
        yield 1
        print('continue')
        yield 2
        print('end')


    ret1 = [item for item in gen_func()]  # 会迫不及待的循环函数体获取生成的值
    ret2 = (item for item in gen_func())
    print('------')
    for i in ret1:
        print(i)
    for i in ret2:
        print(i)

8、 多数据类型等差数列
    def aritprog_gen(begin, step, end=None):
        result = type(begin + step)(begin)
        forever = end is None
        index = 0
        while forever or result < end:
            yield result
            index += 1
            result = begin + step * index

9、内置生成器类型
    itertools.count(start, step) : 生成无穷等差数列
    itertools 模块
    itertools.groupby(iterable, key=None) 按条件对可迭代对象进行分组，条件可以用key参数指定。如果没有指定，就按照元素本身分组
    返回的是一个（key, group), group 是一个迭代器包含组内元素。

    s = 'LLLLAAGGG'
    ret = itertools.groupby(s)
    for key, group in ret:
        print(key)
        for i in group:
            print(i)

10、yield from iterable
    yield from 经常跟一个可迭代对象，会迭代可迭代对象将其内部的值返回。
    等价于
        for item in iterable:
            yield item

11、iter() 有两个用法：
    1、iter(iterable) --> iterator
    2、iter(callable, 标识符) 当可调用对象返回标识符时，抛出一个 StopIteration 的异常。

"""

import re
import random
import reprlib
import itertools
from collections.abc import Iterator
RE_WORD = re.compile(r'\w+')


# 可迭代对象
class Sentence:

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __getitem__(self, item):
        return self.words[item]

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, reprlib.repr(self.text))


# for 循环本质

it = iter((1, 2, 3))
while True:
    try:
        print(next(it))
    except StopIteration:
        del it
        break


# 迭代器
class SentenceIterator:

    def __init__(self, text):
        self.index = 0
        self.words = RE_WORD.findall(text)

    def __next__(self):
        try:
            value = self.words[self.index]
            self.index += 1
        except IndexError:
            raise StopIteration
        return value

    def __iter__(self):    # 迭代器的返回值往往是自己，就是抽象基类实现的那样
        return self


text = 'Return the next,'
s = SentenceIterator(text)
print(isinstance(s, Iterator))
print(next(s))
print(next(s))
print(next(s))
# print(next(s))


# 生成器版本的 Sentence 可迭代对象
class Sentence:

    def __init__(self, text):
        self.words = RE_WORD.findall(text)

    def __iter__(self):
        return (i for i in self.words)


text = 'Return the next,'
s = SentenceIterator(text)
for i in s:
    print(i)


# 惰性运算版的  Sentence 可迭代对象
class Sentence:

    def __init__(self, text):
        self.text = text

    def __iter__(self):
        return (item.group() for item in RE_WORD.finditer(self.text))


# 列表推导式的迫切运算
def gen_func():
    print('start')
    yield 1
    print('continue')
    yield 2
    print('end')


ret1 = [item for item in gen_func()]  # 会迫不及待的循环函数体获取生成的值
ret2 = (item for item in gen_func())
print('------')
for i in ret1:
    print(i)

for i in ret2:
    print(i)


# 自定义一个等差数列 模仿 range(start, stop, step)
class MyRange:

    def __init__(self, start, step, stop=None):
        self.start = start
        self.step = step
        self.stop = stop

    # def __iter__(self):
    #     while self.start < self.stop:
    #         yield self.start          # 只是表明在这个循环体中进行状态的挂起和开启
    #         self.start += self.step   # 选择 self.start 做增量，会改变 self.start 的值
    #                                     # stop 参数没有用上
    def __iter__(self):
        ret = type(self.start + self.step)(self.start)
        index = 0
        forever = self.stop is None
        while forever or ret < self.stop:
            yield ret
            index += 1
            ret = self.start + self.step * index


mr = MyRange(0, 1, 3)
mr2 = MyRange(1, .5, 3)
# mr3 = MyRange(0, 1/3, 1)
print(list(mr))
print(list(mr2))
# print(list(mr3))


# todo 迭代器版本的还是不能实现，当再次看到的时候，请思考下这个功能的实现。
class MyRangeIterator:

    def __init__(self, start, step, stop=None):
        self.start = start
        self.step = step
        self.stop = stop
        self.ret = self.start
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        # if self.ret < self.stop:
        #     yield self.ret
        # else:
        #     return
        # self.index += 1
        # self.ret = self.start + self.step * self.index
        pass


# yield from
it = [(1, 2), (3, 4)]


def foo():
    for i in it:
        yield from i


for i in foo():
    print(i)


# iter() 的另外一个用法
def func():
    return random.randint(1, 3)


ret = iter(func, 2)

print(next(ret))
print(next(ret))
print(next(ret))







