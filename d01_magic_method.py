# todo dunder line method（简单介绍，特殊方法贯穿始终）
"""
1、双下划线方法通常是让解释器调用的，很少直接被使用着调用。如常用len(obj) 而非obj.__len__()来查看一个对象的长度。
2、有些时候，特殊方法的调用是隐式的，如 for i in x: 背后往往实现的是 iter(x), 循环能否顺利执行，要看 x 中是否由
__iter__方法。
3、除非元编程，双下划线方法中使用频率最多就是 __init__方法。建议使用python内置的API去触发这些方法【让解释器去调用】
如 iter(),len()。通常情况下他们会更快更好，当让要重写的场景除外。
4、__str__ 、str()/print的时候会被触发，对象中没有定义__str__时，__repr__会被触发。但如果对象中有__str__方法，
调用 repr()的时候，__str__却不会被触发。

"""
import collections
import random


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '{}({}, {})'.format(type(self).__name__, self.x, self.y)

    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        if not isinstance(other, int):
            raise TypeError('must be int!')
        return type(self)(self.x * other, self.y * other)


v1 = Vector(2, 4)
v2 = Vector(2, 1)
print(v1 + v2)
print(v1 * 3)


# ===================================== review =====================================================
# collections.namedtuple 命名元组
Student = collections.namedtuple('Student', ('name', 'age', 'gender'))  # ('name', 'age', 'gender') 字符串组成的迭代对象
Student = collections.namedtuple('Student', 'name age gender')

ellen = Student('ellen', 18, 'female')
print(ellen)
print(ellen._fields)  # 已元组的形式返回所有的字段名
print(Student._make(['bobby', 13, 'male']))  # 将一个可迭代对象实例化成命名元组对象
print(ellen._asdict())  # 将命名元组对象变成一个OrderDict对象

# list
# 可变序列，支持index, slice[Slice], in, len, +, * ,嵌套列, 列表更新，删除, 可迭代
lst = [i for i in range(10)] + list('abcd')

lst.append('e')
lst.extend(('ha','he', 'xi'))
lst.insert(0, -1)

print(lst.pop(-2))  # 根据索引进行pop， pop后的值会返回出来
lst.append('ha')
lst.remove('ha')  # remove根据值remove第一个匹配到的值，没有返回值
print(lst)
# lst.clear()

print(lst.index('a',2))
print(lst.count('ha'))

print(len(lst))
# print(max(lst))  # 当str 和 int 混合的时候，无法比较，当然也就无法排序
print(lst)
# # min()
# lst.sort(reverse=False)  # True 由大到小
lst.reverse()
print(lst)
# reversed()/sorted() 和 list.reverse/list.sort
# 1.sort 是list的一个方法，sorted接受的是一个可迭代对象
# 2.sort是对原列表进行修改，没有返回值，sorted是会生成一个新列表[reversed 是一个reversed对象]

# random 模块
print('*' * 200)
print(random.random())  # [0,1)
print(random.randint(1, 2))  # [a,b]
print(random.uniform(1.1, 2.5))  # a, b 范围内的随机浮点数
lst2 = [1, 5, 9, 0, 10, 4]
print(random.choice(lst2))
print(random.choices(lst2, k=3))  # 和 sample 的区别就是，choices 可以重复取一个元素，
print(random.sample(lst2, 3))
random.shuffle(lst2)
print(lst2)


Card = collections.namedtuple('Card', ['rank', 'suit'])


class Poker:

    ranks = [str(i) for i in range(2, 11)] + list('JQKA')
    suits = 'flower black kuai red'.split()

    def __init__(self):
        self._card = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __getitem__(self, item):
        return self._card[item]

    def __setitem__(self, key, value):
        self._card[key] = value

    def __len__(self):
        return len(self._card)


poker = Poker()
# 排序rank值大小可以由索引来定，suit需要赋予权重
suit_dict = dict(flower=1, black=2, kuai=3, red=4)


def card_value(card):
    rank_value = Poker.ranks.index(card.rank)
    suit_value = suit_dict[card.suit]
    return rank_value + suit_value


ret = sorted(poker, key=card_value)
print(ret)

random.shuffle(poker)  # TypeError: 'Poker' object does not support item assignment

print(list(poker))
