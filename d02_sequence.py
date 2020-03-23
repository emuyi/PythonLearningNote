# todo sequence [list,tuple]
"""
1、内置数据类型的各种方法要熟悉。
2、列表推导式的一般性原则：用来生成列表。通常情况下要求持代码尽量的简洁，否则影响可读性。！！
3、列表、字典、集合推导式都有自己的局部作用域，不会影响上下文的变量。for循环体，if判断体不是。
4、如果要生成其他序列（非列表）---生成器表达式。
    1、如果生成器表达式是函数的唯一参数，括号可以去掉。2、相比列表推导式，逐一生成值，节省内存。
    tuple(i for i in 'abc')
5、由元组引出拆包，实际上，拆包针对所有的序列及可迭代对象。拆包的一大好处就是增强可读性。！！
    x, *y, z = (1, 3, 4, 5)  y>>>[3, 4]
6、切片：序列的一个重要特性。
    1、前包后不包原则符合python、c下标从0开始的惯例。并且通过首尾下标很容易得出序列的长度。
    2、通过切片赋值可以来修改序列。如 l[2:3] = [100] 但要注意的是，赋值必须是可迭代对象。
    3、使用slice()对象可以创建可读性更好的切片。！！
7、序列的 +、* 以及 +=、*=操作。
    1、嵌套型可变序列使用 * 运算时要注意。[['_'] * 3] * 3 外层重复的是同一个对象。
    2、+=、*=等增量操作，不要再简单的认为就是'加起来再赋值'，它是运算符有着自己的规则。
        a、如果是可变序列：就地运算。相当于a.extend(b)
        b、不可变序列：加起来重新赋值。一般情况下效率是很低的，因为需要新创建一个对象把原来的拿
        过来再把新增的添加上。但字符串的拼接除外，因为太常用所以做了优化。！！！
        c、在元组中尽量不要放可变序列，因为对可变序列的增量操作不是原子性的。如果非要做增量操作
        也不要用 +=、*=，而是使用 a.extend(b)
8、排序：list.sort() / sorted()
    1、sort():是列表的方法, 而且执行的是就地运算。sorted():接收的是任意的可迭代对象, 以列表的形式返回排序结果
    2、都有两个关键字参数：reverse决定是升序排序还是降序排序；key关键字接收一个单参数函数，作用到每个元素，并以
    返回的结果作为排序的条件。
    3、如果要想对一个排好序的序列执行插值操作且保持序列顺序不变。bisect.insort()可以做到。
9、不要总想着用列表去存数据，要学会根据实际场景选择最佳的数据结构。纯数字集合：array，numpy
   首尾频繁操作：deque  集合中是否存在某元素：set
"""
# 拆包可读性
data = [('ellen', 18, ['game', 'movie']),
        ('bobby', 13, ['joke', 'snack'])]

for name, age, [hobby1, hobby2] in data:
    if name == 'bobby':
        print(hobby1)
# namedtuple的3个常见用法
from collections import namedtuple

User = namedtuple('User', 'name pwd phone')
ellen = User('ellen', 12312, 93939)
# cls._make(iters) 类似于 cls(*iters)
bobby = User._make(['bobby', 23423, 909080])
# obj._asdict() 可以将命名元组对象转换为有序字典
print(bobby._asdict())
# obj._fields() 以元组的形式返回所有的字段名

# 可变序列增量运算的 trick
board = [['_'] * 3 for i in range(3)]
board2 = [['_'] * 3] * 3
# board
l1 = []
for i in range(3):
    l1.append(['_'] * 3)
# board2
l2 = []
row = ['_'] * 3
for i in range(3):
    l2.append(row)

# 不要对元组中的序列做增量操作
t = (1, 2, [20, 30])
# t[2] += [40, 50]  # 既会报错也会赋值成功

# 二分查找模块，bisect
import bisect
l = [1, 4, 5, 6, 8, 12, 15, 20, 21, 23, 26]
index = bisect.bisect(l, 22)  # 返回一个index，表示返回位置(index)前的值都小于或等于我要查找的值
# l.insert(index, 22)
# 可以使用bisect找位置，insert插入，但insort会更好。
bisect.insort(l, 22)

# deque
from collections import deque
dq = deque(range(10), maxlen=10)
dq.rotate(3)  # roate(n) 当 n > 0: 将右边的 n 个元素移到左边去；n < 0 反之。
dq.appendleft(-1)  # 当超过队列指定长度是，旧数据会被挤掉，新数据添加进来。
print(dq)

