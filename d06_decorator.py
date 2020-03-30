# todo decorator
'''
1、装饰器接收一个函数（类）作为参数，返回修改后的该函数或者另外一个函数(可调用对象)装饰器可以在
不改变函数调用方式的情况下增强函数的行为。
2、@decorator 语法糖  func = decorator(func)
3、装饰器有两大特性：1、增强函数行为 2、导入时即运行
4、通常情况下：装饰器函数会单独在一个模块中，然后由其他模块的函数调用；并且装饰器函数往往会在内部定义
一个函数并将其返回。但也有直接返回被装饰函数的，如注册类的装饰器，虽然不是经典的装饰器模型，但有其适合
的场景。
5、闭包函数
    1、函数体内如果有赋值操作，那么python在编译函数体的时候就会认为赋值的变量是局部变量。
    使用global关键字可以将其声明为全局变量，然后再使用。
    2、理解闭包，闭包延伸了函数的作用域，能访问非定义体外的非全局变量。因此构成闭包函数往往得是嵌套函数。
    同样，内层函数只能访问外层函数的变量而不能赋值修改，如果想要赋值修改需要使用nonlocal关键字声明变量为
    自由变量。
6、标准库中的装饰器
    functools.wraps/functools.lru_cache/functools.singledispatch
    functools.lru_cache: 递归算法优化
        1、lru算法：最近最少使用，即一段数据最近访问过，那么将来访问的概率也很大。常用来做缓存淘汰策略。
        即缓存中数据满了，根据lru原则，淘汰长时间很少访问的数据来释放缓存空间。可以使用OrderdDict来实现
        lru算法。
        2、lru_cache: 会将比较耗时的函数结果存起来，避免因为传入相同的参数重复计算。有两个关键字
        maxsize=128 如果存放的数据超过maxsize，会淘汰长时间不用的数据。
        typed=False 如果typed为True，会将不同的数据类型单独存放。
        3、注意！lru_cache 内部是用字典来实现的，并且会以函数的参数作为键，因此被装饰的函数的参数必须是可
        散列的。
    functools.singledispath: 单分派泛函数
        可以用来优化 if isinstance()/elif isinstance()/elif isinstance() 这样的根据不同的类型做
        不同处理的结构，主要是提供了一种模块化的解耦。比如说，如果使用if/elif结构，需要将所有的类型全部导入过
        来并且要新增类型，if/elif的代码就得更新一次。如果使用 singledispatch的话，可以把被singdispatch
        装饰的函数导入过来(func) 并且使用 @func.register(NewClass) 注册下新增的类及装饰对应的处理逻辑。
        调用的时候只需要调用func(newObj)即可
7、叠加装饰器和参数化装饰器
    a、叠加装饰器
    @d1
    @d2       ----> func = d1(d2(func))
    func()
    b、参数化装饰器, 往往是一个装饰器工厂函数。
    @d(active=True)
    func()          ---->func = d(active=True)(func)
8、对象版的装饰器 __call__
'''
from functools import wraps, lru_cache, singledispatch

# 经典的装饰器模型
def decorator(func):
    @wraps(func)  # 将被装饰函数的__name__, __doc__等属性复制到inner
    def inner(*args, **kwargs):
        ret = func(*args, **kwargs)
        return ret
    return inner


func_list = []


# 注册类型装饰器
def register(func):
    func_list.append(func)
    return func


@register
def foo():
    pass


@register
def bar():
    pass


# 作用域
b = 3
def func(a):
    print(a)
    global b
    print(b)
    b = 9  # 如果有赋值操作就会被认为是局部变量


func(5)
print(b)

# 计算移动平均值
price_list = []
def average(today_price):
    price_list.append(today_price)
    return sum(price_list) / len(price_list)


print(average(10))
print(average(20))
print(average(30))


# 闭包实现
def make_average():
    price_list = []
    def average(today_price):
        price_list.append(today_price)
        return sum(price_list) / len(price_list)
    return average


avg = make_average()
print(avg(10))
print(avg(20))
print(avg(30))


# 对 sum 做优化
def make_average():
    count = 0
    total = 0

    def average(today_price):
        nonlocal total, count
        total += today_price
        count += 1
        return total / count
    return average


avg = make_average()
print(avg(10))
print(avg(20))
print(avg(30))


# OrderdDict 实现 lru 算法
from collections import OrderedDict


class LRU:

    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.data = OrderedDict()

    def put(self, key, value):
        if len(self.data) >= self.maxsize:
            self.data.popitem(last=False)
            self.data.setdefault(key, value)
        else:
            self.data.setdefault(key, value)

    def get(self, key):
        return self.data.get(key, -1)


lru = LRU(5)
lru.put('a', 1)
lru.put('b', 2)
lru.put('c', 3)
lru.put('d', 4)
lru.put('e', 5)
lru.put('f', 6)
print(lru.data)


@lru_cache()
def fibo(n):
    if n < 2:
        return n
    return fibo(n-2) + fibo(n-1)


# singledispath
import math

@singledispatch
def area(obj):
    raise LookupError('{} not found'.format(obj))


class Circle:
    def __init__(self, r):
        self.r = r


class HAHA:
    pass


@area.register(Circle)
def _(obj):       # 如果注册了直接走注册的逻辑分支，否走area
    return math.pi * (obj.r ** 2)


print(area(Circle(2)))
# print(area(HAHA))

# 参数化装饰器

func_l = []


def register(active=True):
    def decorator(func):
        if active:
            func_l.append(func)
        return func
    return decorator


@register(active=False)
def func1():
    pass


@register()
def func2():
    pass


print(func_l)


# 对象版装饰器
class Decorator:

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print('before func')
        self.func()
        print('after func')


@Decorator
def func3():
    print('func')


func3()