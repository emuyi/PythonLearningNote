# TODO AbstractClass&Inherited
"""
1、关于接口，从语法角度上讲，python中没有接口的概念，因为并没有提供类似 interface 这样的语法去规定什么是接口。与其谈接口，python更接近
   鸭子类型。虽然没有专门的语法，但是可以通过抽象基类来实现类似接口的功能。
2、打补丁：在运行时修改类或者模块，而不改动源码，适用于紧急的问题修复。
    如：poker 不支持shuffle, 是因为 poker 是不可变序列，如果想要可变，就需要实现 __setitem__(self, key, value) 方法，当然可以在
    类中实现，也可以不改动源码的情况下以打补丁的形式实现。

    def setitem_patch(poker, key, value):
        return poker._data[key] = value

    poker.__setitem__ = setitem_patch

3、不要尝试自己定义抽象基类或元类！！！要认清自己的位置。
4、之前自定义的类，在处理接收到参数并没有判断该参数是什么类型，而是利用了鸭子类型。比如按照鸭子类型实现namedtuple()如何接收两种类型参数的。
   如下，这里不是用 if/elif/elif 进行类型的判断，而是定义类型的时候进行逻辑上的处理，让解释器进行分派不同的情况。

   class MyNamedTuple:

        def __init__(self, arg):
            try:
                self.data = arg.split()
            except AttributeError:
                self.data = arg
            self.data = tuple(self.data)


    # mnt = MyNamedTuple('name age hobby')
    mnt1 = MyNamedTuple(['name', 'age', 'hobby'])

    慢慢领悟，慢慢掌握。
5、 抽象基类：如果要继承抽象基类就必须要实现抽象基类中定义的抽象方法。
    抽象基类主要位于 collections.abc / numbers 中
    isinstance(x, numbers.Integral) # 检查是否是整型
    isinstance(x, numbers.Real)  # 检查是否是浮点型
    isinstance(my_obj, Hashable)  # 检查某对象是否可散列
6、 自定义抽象基类
    class ABS(abc.ABC):
                                                        @classmethod
        @abc.abstractmethod              # 定义抽象类方法，@abc.abstractmethod  叠加装饰器
        def abs_method1(self):
            pass

        def normal_method(self):
            .....

    "abc.ABC 是 3.4 后引入的，旧版python写法，metaclass = abc.ABCMeta
    metaclass 是 3 的关键字，2 中是 __metaclass__ = abc.ABCMeta"

5、抽象基类的虚拟子类，不是通过继承的方式，而是通过类注册。即 AbstractClass.register(Clas)(3.3之前)
  通过调用抽象基类的 register 方法可以把一个类中注册为自己的虚拟子类。
  对于虚拟子类，python 在加载或者实例化的时候不会做语法检查并且虚拟子类不能继承抽象基类的任何
  属性和方法。但是虚拟子类可以通过 isinstance/issubclass 测试，但它的__mro__ 查找顺序中
  没有抽象基类。

6、不要继承 python 的内置数据类型，如 str， dict, list, tuple 之类。因为内置类型会忽略子类覆盖的方法。如
    class MyDict(dict):

       def __setitem__(self, key, value):
           super().__setitem__(key, value * 2)


    md = MyDict(a='A')  # {'a': 'A'}  not  {'a':'AA'}

    要用 collections.UserDict, UserList 。。。。等替代

 7、__mro__ 和 super()
    __mro__ : 方法解析顺序，是类的一个属性，返回该类及其所有超类组成的元组，其中元组的顺序就是该类的方法查找顺序。（内部算法：C3算法）
    super():  super() 函数会按照 __mro__ 属性给出的顺序调用超类的方法。 super().method() == super(父类, self).method()

 8、写继承的原则：
      1、一定要先想清楚为什么要用继承实现！
      2、如果两个类之间有明显的 “ 是什么 ” 的关系，那可以做继承。
      3、如果一个类仅仅是为其他类服务，与其他类之间没有关系，只是方便其他类来复用自己的功能，那这个类最好定义为 Mixin 类。
      4、如果一个类是作为接口出现的，那这个类最好定义为抽象基类。
      5、对象组合优于继承。

  9、运算符重载：使自定义的对象能支持 + - * % 之类的运算符操作。
   （广泛来讲，函数调用（()）、属性访问（.）和元素访问 、切片（[]）也是运算符）

  10、运算符重载的原则：（暂时pass）
     1、不能重载内置类型的运算符
     2、不能新建运算符，只能重载现有的
     3、某些运算符不能重载 ——> is、 and、 or 和 not（不过位运算符 &、 | 和 ~ 可以）
     4、始终返回的是一个新对象
"""
import random
import abc
import collections
# random.shuffle((1, 2, 3)) # shuffle(x) x --> 可变序列类型
class A:pass
class B(A):pass


b = B()
print(isinstance(b, B))


# python 的多态和鸭子类型
class MyNamedTuple:

    def __init__(self, arg):
        try:
            self.data = arg.split()
        except AttributeError:
            self.data = arg
        self.data = tuple(self.data)


# mnt = MyNamedTuple('name age hobby')
mnt1 = MyNamedTuple(['name', 'age', 'hobby'])


# 自定义抽象基类
class ABS(abc.ABC):

    @abc.abstractmethod
    def abs_method1(self):
        pass

    def normal_method(self, x, y):
        print(x + y)


class C(ABS):

    def abs_method1(self):
        print('ccccccccccccccccccc')


c = C()
c.abs_method1()
c.normal_method(1, 2)


@ABS.register
class D:

    pass


d = D()
# d.normal_method()


# 忽略覆盖的方法
class MyDict(dict):

   def __setitem__(self, key, value):
       super().__setitem__(key, value * 2)


md = MyDict(a='A')  # {'a': 'A'}  not  {'a':'AA'}
md['b'] = 'B'
print(md)
md.update(c='C')
print(md)   # {'a': 'A', 'b': 'BB', 'c': 'C'}


class MyDict2(collections.UserDict):

    def __setitem__(self, key, value):
        super().__setitem__(key, value * 2)


md2 = MyDict2(a="A")
print(md2)


# super()
class A:
    def ping(self):
        print('ping:', self)


class B(A):
    def pong(self):
        print('pong:', self)


class C(A):
    def pong(self):
        print('PONG:', self)


class D(B, C):
    def ping(self):
        super().ping()
        print('post-ping:', self)

    def pingpong(self):
        self.ping()
        super().ping()
        self.pong()
        super().pong()
        C.pong(self)


print(D.__mro__)
d = D()
d.ping()
d.pingpong()
