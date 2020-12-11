import re
import collections

i = iter(range(10))
# print(next(i))
# print(next(i))

# 迭代常常是隐形的。模拟 for i in xxx:


def for_simulator(iterable):
    iterator = iter(iterable)
    while True:
        try:
            print(next(iterator))
        except StopIteration:
            break


for_simulator(range(10))


# poker game

Cards = collections.namedtuple('Card', 'rank suit')


class Poker:

    ranks = [str(i) for i in range(2, 11)] + list('JQKA')
    suits = 'flower red black kuai'.split()

    def __init__(self):
        self._cards = [Cards(rank, suit) for suit in self.suits for rank in self.ranks]

    def __getitem__(self, item):
        return self._cards[item]

    def __len__(self):
        return len(self._cards)


poker = Poker()
print(poker[-1])
# 做排序处理

suit_values = {'flower': 1, 'red': 2, 'black': 3, 'kuai': 4}


def card_value(card):
    rank_value = Poker.ranks.index(card.rank)
    suit_value = suit_values[card.suit]
    return rank_value + suit_value


print(sorted(poker, key=card_value))

# Slice()
s = '---------ellen-------12---'
name = slice(9, 14)
age = slice(-5, -3)
print(s[name], s[age])
print('=' * 100)
# re
s = "12112asdfs we."
matches = re.finditer(r'\w+', s)
for match in matches:
    print(match.group())
    print(match.start())

"""
现有一个列表li = [1,2,3,'a',4,'c'],有一个字典(此字典是动态生成的，你并不知道他里面有多少
键值对，所以用dic={}模拟字典；现在需要完成这样的操作：如果该字典没有"k1"这个键，那就创建
这个"k1"键和对应的值(该键对应的值为空列表)，并将列表li中的索引位为奇数对应的元素，添加到
"k1"这个键对应的空列表中。如果该字典中有"k1"这个键，且k1对应的value是列表类型。那就将该列表li
中的索引位为奇数对应的元素，添加到"k1"，这个键对应的值中。
"""
li = [1,2,3,'a',4,'c']
dic = {}
dic.setdefault('k1', []).extend(li[::2])
print(dic)

# 阶乘 n!
from functools import reduce
ret = reduce(lambda x, y: x + y, range(5))

# 递归的写法


def fact(n):
    return 1 if n < 2 else n * fact(n-1)


def fact2(n):
    a = 1
    for i in range(1, n+1):
        a *= i
    return a


print(list(map(fact, range(1, 10))))
print(list((fact(n) for n in range(1, 10))))
print(list(map(fact2, range(1, 10))))
print(list((fact2(n) for n in range(1, 10))))

import random


class RandomPick:

    def __init__(self, iterable):
        self.iterable = list(iterable)
        random.shuffle(self.iterable)

    def __call__(self, *args, **kwargs):
        return random.choice(self.iterable)


pick = RandomPick([1, 2, 3, 4])
print(pick())
print(pick())


# clip 在max_len前面或后面的第一个空格处截断文本

def clip2(text, max_len=5):
    """在指定长度前后空白除截断文本"""
    end = None
    if len(text) > max_len:
        space_before = text.rfind(' ', 0, max_len)
        if space_before >= 0:
            end = space_before
        else:
            space_after = text.rfind(' ', max_len)  # end 不传默认是到最后
            if space_after >= 0:
                end = space_after
    if end is None:  # 没找到空格
        end = len(text)
    return text[:end].rstrip()


text = 'wef wefw ojiojoj'


def clip(text, max_len=5):
    ret_index = None
    if len(text) > max_len:
        space_before = text.find(' ', 0, max_len)
        if space_before != -1:
            ret_index = space_before
        else:
            space_after = text.find(' ', max_len)
            if space_after != -1:
                ret_index = space_after
    if ret_index is None:
        ret_index = len(text)
    return text[:ret_index].strip()


print(clip(text))


# decorator
def decorator(func):
    def inner(*args, **kwargs):
        print(1111111111111)
        # ret = func(*args, **kwargs)
        return ret
    return inner


@decorator  # test = decorator(test)
def test(x, y):
    print(222222222222)
    print(x + y)


test(2, 4)
# 求移动均价
price_list = []


def avg(price):
    price_list.append(price)
    return sum(price_list) / len(price_list)


def make_average():
    price_list = []
    def average(price):
        price_list.append(price)
        return sum(price_list) / len(price_list)
    return average

avg = make_average()
print(avg(10))
print(avg(11))
print(avg(12))

# LRU 算法实现
from collections import OrderedDict
class LRU:

    def __init__(self, maxsize=10):
        self.maxsize = maxsize
        self.data = OrderedDict()

    def put(self, key, value):
        if len(self.data) > self.maxsize:
            self.data.popitem(last=False)
        self.data[key] = value

    def get(self, key):
        return self.data.get(key, None)

# 两种方式实现斐波那契数列
def fibo(n):
    return n if n < 2 else fibo(n-1) + fibo(n-2)

def fibo2(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a+b
    return a

# singledispatch
from functools import singledispatch


@singledispatch
def print_func(arg):
    print('你没注册，走我这边')



@print_func.register(str)
def _(arg):
    print('str 应该有的打印格式')


@print_func.register(list)
def _(arg):
    print('list 应该有的打印格式')



# =========================================
import math
@singledispatch
def area(obj):
    raise LookupError(' Not register')



class Circle:

    def __init__(self, r):
        self.r = r



@area.register(Circle)
def _(obj):
    print(math.pi * (obj.r**2))


print_func('1')
print_func([1, 2, 3, 4])
area(Circle(1))

# 带参数的注册类型装饰器

data_list = []


def decorator(active=True):
    def register(func):
        print('带参数的装饰器')
        if active:
            data_list.append(func)
        return func
    return register


@decorator()
def foo():
    print('foo is running')


@decorator(active=False)
def bar():
    print('bar is running')


print('=' * 100)
foo()
bar()
print(data_list)
print(foo.__name__)

