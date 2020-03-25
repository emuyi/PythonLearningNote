# todo functional programming
"""

1、函数内省
  func.__code__：存放函数体信息（名称，参数）
  如果想提取一个函数的信息 ————内置模块inspect
2、参数注解
    def clip(text:str, max_len:'int > 0'=5) -> str:
    仅供IDE、框架调用获取函数信息、python不做任何的检查
3、内置函数式编程模块
    operator:
        1、mul: 搭配reduce实现阶乘 operator 有很多关于运算符的函数
        2、itemgetter: 获取序列或者可迭代你对象的元素，常和内置的那几个高阶函数一块使用
        用来替代lambda表达式 如：sorted(seq, key=itemgetter(1))
        并且 itemgetter 可以获取多个元素 如：itemgetter(1,2)(seq)
        3、attrgetter: 根据对象属性名称获取对象属性，和 itemgetter的用法一样。
        不过是一个获取序列的元素一个是获取对象的属性。
    functools:
        1、reduce：求和、阶乘
        2、partial & partialmethod：偏函数（冻结部分参数）首先是一个高阶函数
        partial(func, args, kwargs) 创建一个函数，调用的时候只需要传入部分参数
        如：p = partial(func, 3)   p(2)
        partialmethod : 和partial 一样，不过是冻结方法的参数 注意！要在类内创建

"""

# 剪切函数，用指定长度截断字串
data_list = []
def clip(text:str, max_len:'int > 0'=5) -> list:
    """适用于理想文本状态"""
    start = 0
    end = max_len
    for i in range(int(len(text) / max_len) + 1):
        data = text[start:end]
        data_list.append(data)
        start += max_len
        end += max_len   # todo python 对字符串切片越界的情况做了优化
    return data_list     # 理清需求，多写写画画帮助理顺逻辑


text = 'qqrweqweeeeee'
print(clip(text))


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


text = 'qqr weqwe eeeee'
print(clip2(text))
print(clip2.__defaults__)
print(clip.__code__.co_varnames)

# operator
from operator import mul, itemgetter, attrgetter
from functools import reduce, partial, partialmethod


def fact(n):
    return reduce(mul, range(1, n+1))  # mul == lambda x,y :x *y


print(fact(3))
metro_data = [
('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833))]

# 根据 36.933 字段给列表排序

metro_data_new = sorted(metro_data, key=lambda x:x[2])
metro_data_new2 = sorted(metro_data, key=itemgetter(2))
print(metro_data_new2)
"""
from operator import itemgetter, attrgetter
t = tuple('abc')
>>>itemgetter(0,1)
>>>operator.itemgetter(0, 1)
>>>itemgetter(0,1)(t)
>>>('a', 'b')
"""


# attrgetter 对象版的itemgetter
class User:

    def __init__(self, name, age, hobby):
        self.name = name
        self.age = age
        self.hobby = hobby

    def __repr__(self):
        return self.name


ellen = User('ellen', 18, 'game')
bobby = User('bobby', 13, 'joke')
hank = User('hank', 38, 'fishing')

print(sorted([ellen, bobby, hank], key=attrgetter('age')))
print(list(map(attrgetter('name', 'hobby'), [ellen, bobby, hank])))

# partial


def func(x, y):
    return x * y


partial_func = partial(func, 3)
print(list(map(partial_func, range(1, 10))))


class A:

    def method(self, x, y):
        return x * y
    partial_method = partialmethod(method, 3)  # todo


# 类外调用不是callable对象
a = A()
print(list(map(a.partial_method, range(1, 10))))

