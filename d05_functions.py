# todo functional programming
"""
1、函数是一等对象
    a.能赋值给变量，能作为其他数据结构的元素。
    b.能做函数的参数
    c.能做函数的返回值
2、b,c 合起来可以构成高阶函数。即接收一个函数作为参数或者返回一个函数的函数。内置的像map，filter，reduce
sorted，max，min 装饰器
3、map，filter的直接替代品 -- 生成器表达式。相比着lambda表达式可读性更好。
4、functools.reduce 主要作用就是求和，3版本以来，用sum()求和更好。
  reduce 和 sum 都是归一函数：把一系列的值整合成一个结果。此外还有 any()/all()
5、匿名函数。受python语法限制，lambda表达式要尽量简洁，如果比较复杂请用def实现。lambda表达式常作为高阶函数的
  参数使用，如果map/filter/sorted
6、如果一个对象要可调用，内部需实现 __call__方法。如装饰器的面向对象写法。可以使用callable()判断一个对象是否时可调用对象
7、*args和**kwargs 除了基本的用法外，还需要注意一点就是：传参的时候，实参关键字参数形式可以给位置参数传参，注意
得是同名的位置参数。
    def func(arg, *, kwarg):
        print(arg)
        print(kwarg)
    func(1, kwarg=2)
8、函数内省
  func.__code__：存放函数体信息（名称，参数）
  如果想提取一个函数的信息 ————内置模块inspect
9、参数注解
    def clip(text:str, max_len:'int > 0'=5) -> str:
    仅供IDE、框架调用获取函数信息、python不做任何的检查
10、内置函数式编程模块
    operator:
        1、mul: 搭配reduce实现阶乘 operator 有很多关于运算符的函数
        2、itemgetter: 获取序列中的某个元素，常和内置的那几个高阶函数一块使用
        用来替代lambda表达式 如：sorted(seq, key=itemgetter(1))
        原理：itemgetter(index1, index2..) 是一个可调用对象，调用的时候接收一个seq做为参数，然后执行 seq[index] 的操作。
        3、attrgetter: 根据对象属性名称获取对象属性，和 itemgetter的用法一样。
        不过是一个获取序列的元素一个是获取对象的属性。
    functools:
        1、reduce：常用来求和（sum） 和 求阶乘
        2、partial & partialmethod：偏函数（冻结部分参数）首先是一个高阶函数
        partial(func, args, kwargs) 创建一个函数，调用的时候只需要传入部分参数
        如：p = partial(func, 3); p(2)
        partialmethod : 和partial 一样，不过是冻结方法的参数 注意！要在类内创建
        class B:
            def method(self, x, y):
                return x + y
            partial_method = partialmethod(method, 1)

        b = B()
        ret = b.partial_method(3)

"""
# 阶乘
import random
from functools import reduce
# reduce 实现
print(reduce(lambda x, y: x * y, range(1, 10)))


# map 及生成器表达式
def fact(n):
    return n * fact(n - 1) if n > 1 else n


print(list(map(fact, range(1, 10))))
print(list((fact(n) for n in range(1, 10))))


# __call__
class Item:

    def __init__(self, iterable):
        self.data = list(iterable)
        random.shuffle(self.data)

    def __call__(self, *args, **kwargs):
        try:
            ret = self.data.pop()
        except IndexError:
            raise LookupError('pop from empty list')
        return ret


item = Item([])
# item()

data_list = []


# 剪切函数，用指定长度截断字串
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
# print(clip2.__defaults__)
# print(clip.__code__.co_varnames)

# operator
from operator import mul, itemgetter, attrgetter
from functools import reduce, partial, partialmethod


def fact(n):
    return reduce(mul, range(1, n+1))  # mul == lambda x,y :x *y


print(fact(3))

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

# ===================================== review ================================================================


def func(arg, *args, kwarg=None, **kwargs):
    print(arg)
    print(args)
    print(kwarg)
    print(kwargs)


func(1, 2, 3, 4, kwarg=5, **dict(a=1, b=2, c=3))


def func(arg, kwarg=None):
    print(arg)
    print(kwarg)


func(5, 6)


def func(arg, *, kwarg):
    print(arg)
    print(kwarg)


func(1, kwarg=2)


# 三种方式实现阶乘
# 递归
def f1(n):
    return 1 if n < 2 else n * f1(n - 1)


def f2(n):
    return reduce(mul, range(1, n+1))


def f3(n):
    ret = 1
    for i in range(1, n+1):
        ret *= i
    return ret


print(f1(5), f2(5), f3(5))

print('===========================================')
# itemgetter
from operator import itemgetter, attrgetter
ret = itemgetter(0, 2, 3)('abcdefg')
print(ret)
metro_data = [
('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833))]

# 根据 36.933 字段给列表排序
metro_data_new = sorted(metro_data, key=lambda x:x[2])
metro_data_new2 = sorted(metro_data, key=itemgetter(1, 2))
print(metro_data_new2)
from functools import partial, partialmethod


# 偏函数(冻结部分参数)
def func(a, b, c):
    print(a, b, c)


partial_func = partial(func, 2, c=3)
partial_func(1)


# 必须要在类中定义 partialmethod
class B:

    def method(self, x, y):
        return x + y
    partial_method = partialmethod(method, 1)


b = B()
ret = b.partial_method(3)
print(ret)