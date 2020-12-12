# TODO class&object
"""
1、变量从来不是容器，而是标注，引用。a=[], b=a, a is b
2、 is & == ， is 比较的是内存地址，是不是同一个对象；== 比较的是值是否相等，即存的数据是不是一样的。
    (is None/is not None)
3、 浅拷贝&深拷贝
    浅拷贝：对于大多数的可变序列来讲，除copy.deepcopy，大多做的都是浅拷贝，如常使用构造方法或者seq[:]
    (这里需要注意：针对的是可变数据类型!!)
    浅拷贝一个原可变序列的副本。浅拷贝出来的副本和源数据共享内部对象的引用，所以当内部对象有可变数据类型时要注意。
    深拷贝：copy.deepcopy
4、 不要使用可变数据类型作为函数的默认值。常用 None 做默认值，然后再对 None进行判断处理。
    函数在处理接收的参数时，要注意考虑如果参数是可变数据类型，是否要
    涉及到原参数的修改，如果不涉及，是否考虑过有对参数做副本处理。如 list(seq) or ....
5、 垃圾回收机制，cpython解释器中主要还是是通过引用计数法来判断一个对象是否应该被回收释放。当一个对象的引用数量为0时，
    python 会对对象进行回收释放。因此， del var 以及对对象重新赋值，其实都是在删除对对象的引用。
    （Tips：不要轻易尝试自己实现__del__, 因为大多时候都是弄巧成拙。)

6、pythonic object (dunder method)
   @classmethod: 和对象无关，和类有关的方法
   @staticmethod: 定义在类中的普通函数

7、如何实现一个可散列的对象. 1.__hash__(), 2.__eq__(), 3.在整个生命周期中对象不能发生变化
   @property: 以调用属性的形式调用对象方法，常和私有属性配合使用，将某一属性变成只读属性

8、 私有属性 self.__x 是通过名称改写的方式来避免属性在类外直接被调用。类外通过 obj._类名__属性名 的方式任然可以访问，
    也有 self._x 的方式从字面意义上来表示该属性私有。

9、 __slots__ 主要是用来做内存优化。因为 python在存储属性的时候是通过字典来存，如果定义了__slots__，python在存储对象属性的时候
    会换成元组来存储，从而减少内存消耗。
    __slots__ = ('name', 'age', 'hobby')  # 我所有的属性都在这啦！
    特点：1、__slots__ 不能继承，如果要想要在子类中使用的话，需要在子类中实现
         2、经过__slots__ 限制之后，对象就不能新增属性，如果想要新增属性，需要在__slots__ 中添加__dict__, 这意味着新增属性
           的存储方式还是字典，这时候就要根据需求来考虑__slots__使用的必要性。
         3、如果想保持对象弱引用属性的话，注意在__slots__中添加 __weakref__ 属性
         4、__slots__ 的意义在于内存优化，而不是限制新增对象属性。
10、用类来修改类属性，对象覆盖的类属性其实是自己的属性。
11、reprlib.repr() 限制输出字符串的长度，用... 表示截断部分。
12、序列协议：对象内部实现了__getitem__, __len__ 方法。当我们自定义的对象内部实现了__getitem__, __len__ 方法，那这个对象看上去就是
    一个序列，不是指这个对象就是序列，而是这个对象具有序列的行为，这就是python中常说的鸭子类型。
13、序列切片的原理：__getitem__(self, index) 如果 index 是单个数字是按索引取值，如果是seq[start:stop:step] 的形式，会被整合成
    seq.__getitem__(self, slice(start, stop, end)) 的形式。
14、slice() 对切片命名，避免切片的硬编码，slice.indices(指定长度)
    >>> a = slice(5, 50, 2)
    >>> s = 'HelloWorld'
    >>> a.indices(len(s))
    >>> (5, 10, 2)

15、__getattr__ / __setattr__
    getattr: 当获取对象中不存在的属性时，会调用 getattr
    setattr: 当给对象添加属性, 更改属性值时会被调用 （本质上是在管理 self.__dict___） 利用 __setattr__ 可以给对象设置只读属性
    也可以禁止对象新增属性。

16、functools.reduce
    把一系列值归约成单个值。 reduce() 函数的第一个参数是接受两个参数的函数，第二个参数是一个可迭代的对象,
    第三个参数是当可迭代对象为空时，设置的初始值。
    TypeError: reduce() of empty sequence with no initial value

17、如何高效的对两个或多个可迭代对象做等值测试？
    1、判断长度
    2、判断内部元素
    一行代码：len(iter1) == len(iter2) == len(iter3) and all(x == y == z for x, y, z in zip(iter1, iter2, iter3))
    zip(iterable...) 可以并性迭代两个或多个可迭代对象，返回的元组可以拆包成变量，分别对应每个并行迭代的元素。
    itertools.ziplongest(iterable..., fillvalue=xx)
"""

from functools import reduce
from operator import xor
# 不要使用可变数据类型作为函数的默认参数
class Subway:

    def __init__(self, passengers=[]):
        self.passengers = passengers

    def pick(self, passenger):
        self.passengers.append(passenger)

    def drop(self, passenger):
        self.passengers.remove(passenger)


sub1 = Subway(['ellen', 'bobby', 'joe', 'jane'])
sub1.drop('ellen')
sub1.pick('alex')
print(sub1.passengers)
sub2 = Subway()
sub2.pick('amy')
sub3 = Subway()
sub3.pick('jode')
print(sub2.passengers)  # ['amy', 'jode']
print(sub3.passengers)  # ['amy', 'jode']   passengers 指向的是同一个列表对象


# 当传入的数据类型为可变数据类型的时候，要根据实际情况考虑是否要做副本处理
class Subway:

    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = passengers

    def pick(self, passenger):
        self.passengers.append(passenger)

    def drop(self, passenger):
        self.passengers.remove(passenger)


team = ['ellen', 'bobby', 'joe', 'jane']
sub4 = Subway(team)
sub4.drop('jane')
sub4.drop('joe')
print(sub4.passengers)
print(team)  # ['ellen', 'bobby'] 难道下车了就要从队伍中除名么？所以, self.passengers = list(passengers)

# str, bytes, tuple 浅拷贝"骗局"
t1 = (1, )
t2 = tuple(t1)
t3 = t1[:]
print(t1 is t2 is t3)   # True


# pythonic object
class Vector2d:

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __iter__(self):
        return iter((self.x, self.y))   # (i for i in (self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __bool__(self):
        return bool(self.x or self.y)

    # def __setattr__(self, key, value):         # 1、如果要让一个对象属性可读，这样处理为什么不行？
    #     raise AttributeError('cant set attribute')

    def __repr__(self):
        return '{}({},{})'.format(type(self).__name__, self.x, self.y)

    def __str__(self):
        return '({},{})'.format(self.x, self.y)  # str(tuple(self)) 因为可迭代


v = Vector2d(1, 2)


# 只读属性的 Vector2d
class Vector2d:

    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y


class A:

    @classmethod
    def clsmethod(*args):  # (<class '__main__.A'>, 1)
        print(args)

    @staticmethod
    def stamethod(*args):
        print(args)


a = A()
print(a)
a.clsmethod(1)
a.stamethod(1)


# __slots__
class Person:

    __slots__ = ('name', 'age', 'gender', '__dict__', '__weakref__')

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender


p = Person('ellen', 18, 'female')
p.name = 'bobby'
p.hobby = 'TV'
print(p.__dict__)

import reprlib, numbers


class Vector:

    attrs = 'xyzt'

    def __init__(self, iterable):
        self.data = [float(i) for i in iterable]  # dataType 可否考虑过数组

    def __iter__(self):
        return (i for i in self.data)   # iter(self.data)

    # def __eq__(self, other):   # 存在效率问题
    #     return tuple(self.data) == tuple(other)

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for a, b in zip(self, other):
            if a != b:
                return False
        return True          # return len(self) == len(other) and all(a = b for a, b in zip(self, other))

    def __bool__(self):
        if not self.data:
            return all(self.data)   # 存疑，因为不清楚多维向量真假辨别方式
        return False

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, reprlib.repr(self.data))

    def __str__(self):
        return str(tuple(self))

    # 使 Vector 看起来像是序列
    # def __getitem__(self, item):
    #     return Vector(self.data[item])   # 你是否忘记了使用索引取值的情况

    def __getitem__(self, item):
        if isinstance(item, slice):
            return Vector(self.data[item])
        elif isinstance(item, numbers.Integral):
            return self.data[item]
        else:
            raise TypeError('must be integer!!!')

    # 以 x, y, z, t 为属性，访问前四个分量的值  1、可以做4个 @property 来处理

    # def __getattr__(self, item):
    #     index = self.attrs.find(item)  # 有没有考虑到对 item 长度的限定
    #     if index != -1:
    #         return self.data[index]   # !有没有考虑到边界问题， 不仅仅为拘泥于功能的实现，而是将问题抽象起来，这是一种需要持续培养的能力
    #     raise LookupError('no such attr!')
    def __getattr__(self, item):   # 仍然会有问题，想下 getattr 的处理机制
        if len(item) == 1:
            index = Vector.attrs.find(item)
            if 0 <= index < len(self.data):
                return self.data[index]
        raise AttributeError('No such attribute!')

    def __setattr__(self, key, value):  # 处理上方问题，将 attrs 冻结不允许修改值，同时限制给对象新添加指定类型的属性值
        if len(key) == 1:
            if key in Vector.attrs:
                error = 'readonly attribute'
            elif key.islower():
                error = 'No lower!'
            else:
                error = ''
            if error:
                raise AttributeError(error)

        super().__setattr__(key, value)   # 运行 v 有正常的添加属性操作

    def __len__(self):
        return len(self.data)

    def __hash__(self):
        hash_values = map(hash, self.data)
        return reduce(xor, hash_values)


v = Vector(range(1, 10))
print(v[-1])
print(v.x, v.y, v.z, v.t)

v.x = 10
print(v.x)  # 10
print(repr(v))  # Vector([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, ...])




# 切片原理
class B:

    def __getitem__(self, index):
        return index


b = B()
print(b[-1])
print(b[1:4:2])
print('=' * 150)
# 理解 getattr 和 setattr


class User:

    def __init__(self, name):
        self.name = name       # 走 settattr

    def __getattr__(self, item):
        print('---getattr---')
        return 1

    def __setattr__(self, key, value):
        print('---setattr---')
        self.__dict__[key] = value   # __setattr__ 管理的是 self.__dict__


ellen = User('ellen')
print(ellen.name)
ellen.age = 18
print(ellen.age)
ellen.age = 16
print(ellen.age)
print(ellen.hobby)