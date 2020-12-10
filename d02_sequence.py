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
10、关于序列可分为（list，tuple, collections.deque) 存放多种数据类型；存储的是指向元素的引用。
    （str, bytes, array.array, bytesarray, memoryview） 存放一种数据类型；存储的是元素本身。
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

# ===================================== review =====================================================
# 1、列表推导式主要是用来生成列表，尽量保证简洁和可读性
# 2、过滤或整合其他序列或可迭代对象中的元素（map; filter; reduce; zip; zip_longest;）
# 3、生成器表达式，惰性运算，解决内存。如果生成器表达式是另外一个函数的唯一参数，那么可以不用带双括号
'''
4、元组
    :不可变列表
    :没有字段名的记录
        元组拆包--> 可迭代对象拆包(唯一条件就是拆的变量要和元素对应起来，剩的多余的可以用 *varname 来接收)

5、切片，[a:b:s] s 的正负只和取值的方向有关，仅此而已。
   slice 对象：相比切片，增强可读性，避免硬编码.
   对切片进行赋值可以对原可变序列进行修改，但注意：赋的值一定得是可迭代序列

6、序列拼接
    序列可以进行拼接操作，即 + / * 序列拼接操作的一个基本原则就是生成新的序列不改变原序列，
    但对于某些可变序列如列表中生成列表使用拼接时就会出现意想不到的问题，[[]*3]*3 --> 得到
    的列表中的元素其实是引用，指向的是同一个列表。所以当生成列表中套列表时，推荐使用列表生成式。
    
7、序列的增量赋值（+=， *=）即: a += b 并非简单的 a = a + b 
   这需要看 a 是否可变。
   a 可变序列类型，会调用 a 内部的 __iadd__方法，实现就地增加，修改的是原来 a 的值
   a 不可变序列类型，内部没有 __iadd__ 方法，a+=b 就是单纯的 a = a + b 但是这样进行增量操作效率会很低，字符串类型除外。
   
   一个奇怪的地方：
   t1 = (1, 2, [100])
   t1[2] += [200]
    Traceback (most recent call last):
    File "<input>", line 2, in <module>
    TypeError: 'tuple' object does not support item assignment
    print(t1) >>>> (1, 2, [100, 200])
    那如何正确操作：
    
8、list.sort/sorted

    !!!! 一个典型的for循环中通过索引删除或增加元素出现的问题!!!!!
    
    # sorted
    l8 = [1, 2, 'ab', 'c', 5, 6]
    
    for index in range(len(l8)):
        if isinstance(l8[index], str):
            # print(l8[index])
            # print(index)
            l8.pop(index)
    
    """
    Traceback (most recent call last):
      File "D:/Learning/python-learning-notes/d02_sequence.py", line 262, in <module>
        if isinstance(l8[index], str):
    IndexError: list index out of range
    
    """

9、bisect 二分查找算法模块
    
  bisect.bisect_left(seq, value)   如果有序序列中存在要插入的值 value，那么将返回到已存在值的左边一位的索引
  bisect.bisect_right/bisect.bisect 右边
  
  bisect.insort_left(seq, value)  如果有序序列中存在要插入的值 value，那么将插入到已存在值的左边
  bisect.insort_right/bisect.insort 右边 （先bisect O(logN)  再 insert O(N)）
  
  
    scores = [33, 99, 77, 70, 89, 90, 100]


    def grades(score, breakpoints=(60, 70, 80, 90), mark='FDCBA'):
        i = bisect.bisect_left(breakpoints, score)
        return mark[i]


    print([grades(score) for score in scores])
    
  # 任何一个需求都可以有不同的角度去思考，当你的思考走到一个很复杂的角度时，
  # 有没有考虑过深吸一口气，完全抛弃原来的角度，重新去思考需求和问题。

10、不要太依赖列表
    当处理的是大量的数字类型数据时，用 array 来处理要好很多；需要频繁首尾操作的时候 deque；当频繁检查元素成员关系时，可以使用 set
    array.array(typecode, iterable)
    
    array 几乎支持列表的所有操作，即便是 bisect.insort; 但不支持list.sort 原地排序，如果需要对array进行排序，得使用 sorted
    重新生成 array 即：array.array(a.typecode, sorted(a))
    
    array 还支持直接从文件中读取数据或者存入数据到文件
    
    data = array.array('d', [random.random() for i in range(10**7)])  # 1.4262282848358154
    # data = [random.random() for i in range(10**7)]  # 1.085099458694458
    print(data[-1])
    f = open('float', 'wb')
    data.tofile(f)
    # 取
    array_data = array.array('d')
    f = open('float', 'rb')
    array_data.fromfile(f, 10**7)
    print(array_data[-1])

11、memoryview 和 numpy/sicpy [存储/处理数字类型]
12、 deque
    from collections import deque

    dq = deque(range(10), maxlen=10)  # 同过 maxlen 可以实现保存最近使用的数据
    dq.append(10)
    dq.pop()
    dq.appendleft(0)
    dq.extend([10, 11, 12])
    dq.extendleft([-1, -2])
    dq.rotate(-4)  # n > 0 将后面n个移到前面，n < 0 将前面的n个移到后面
    print(dq)
    
        

'''
# 相关面试题：
# [[0,0,0,0,0,],[0,1,2,3,4,],[0,2,4,6,8,],[0,3,6,9,12,]]
print([[0 for i in range(5)], [i for i in range(5)],
       [i for i in range(9) if i % 2 == 0], [i for i in range(13) if i % 3 == 0]])

# Answer:
list1 = [[i * j for j in range(5)] for i in range(4)]
print(list1)

# 给定两个list A = [1,2,3,4,5,6,7,1,2,3]和B=[4,5,6,7,8,9,10,9,8,11],
# 请用python找出A,B 中相同的元素放入列表D中，找出A,B中不同的元素放入列表C中，确保C、D两个列表中的元素不重复（用代码实现）

A = [1,2,3,4,5,6,7,1,2,3]
B = [4,5,6,7,8,9,10,9,8,11]

D = list(set(A) & set(B))
print(D)
C = list(set(A) - set(B)) + list(set(B) - set(A))
print(C)

# Answer:
D = [i for i in A if i in B]
# C = list(set([i for i in A if i not in B] + [j for j in B if j not in A]))
C = [x for x in set(A + B) if x not in D]
print(D)
print(C)

# unicode > 127 的找出来
symbols = '$¢£¥€¤'
print([i for i in symbols if ord(i) > 127])
print(list(filter(lambda x: ord(x) > 127, symbols)))

t = tuple(range(10))
print(len(t))
print(sorted(t))
print(t.count(1))
print(t.index(5))
print(t[-1])
print(t[::-1])
print(max(t))

print('*' * 100)


name, age, hobby, [x, y] = ('ellen', 18, 'reading', ['1', '2'])
a, b, c, d = 'abcd'
a, b, *rest = 'abcd'

metro_areas = [
('Tokyo','JP',36.933, (35.689722, 139.691667)),   # 把最后一位数字<10的筛选出来
('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]


def main(areas):
    ret = []
    for city, country, num, (i, j) in metro_areas:
        if j < 0:
            ret.append((city, country, num, (i, j)))
    return ret


print(main(metro_areas))


MetroAreas = namedtuple('MetroAreas', 'city country num coordinate')

new_metro_areas = [MetroAreas(city, country, num, (x, y))for city, country, num, (x, y) in metro_areas]
print(new_metro_areas)

for new_metro_area in new_metro_areas:
    print(new_metro_area._fields)
    print(new_metro_area._asdict())  # 有序字典


print(MetroAreas._make(['beijing', 'CN', 100, (2, 3)]))

# Slice
l1 = list(range(100))
l2 = slice(10, 20)
print(l1[l2])

# 切片赋值注意事项
l3 = list(range(10))
# l3[2:3] = 200  NO!!!!!!!!
l3[2:3] = (200,)
print(l3)

# 序列拼接
l4 = [[100] * 4] * 4
l4[0][0] = 200  # [[200, 100, 100, 100], [200, 100, 100, 100], [200, 100, 100, 100], [200, 100, 100, 100]]

l5 = [100] * 4
ret = []
for i in range(4):
    ret.append(l5)

# 所以当生成列表中套列表时，推荐使用列表生成式
l6 = [[100] * 4 for i in range(4)]
l6[0][0] = 200
print(l6)


ret = []
for i in range(4):
    l5 = [100] * 4
    ret.append(l5)

# 序列的增量操作
l7 = [1, 3]
s = 'a'
print(id(l7))
print(id(s))
l7 += [4, 5]
s += 'b'
print(id(l7))
print(id(s))

# 陷阱 元组中存列表
t1 = (1, 2, [100])
# t1[2] += [200]
# print(t1)
"""
t1 = (1, 2, [100])
... t1[2] += [200]
Traceback (most recent call last):
  File "<input>", line 2, in <module>
TypeError: 'tuple' object does not support item assignment
t1
(1, 2, [100, 200])
"""
# sorted
l8 = [1, 2, 'ab', 'c', 5, 6]

ret = sorted(filter(lambda x: isinstance(x, int), l8))
# print(sorted(l8, key=lambda x: isinstance(x, int)))

# for index in range(len(l8)):
#     print(index)
#     if isinstance(l8[index], str):
#         # print(l8[index])
#         # print(index)
#         l8.pop(index)

"""
Traceback (most recent call last):
  File "D:/Learning/python-learning-notes/d02_sequence.py", line 262, in <module>
    if isinstance(l8[index], str):
IndexError: list index out of range

"""
print('----------------------------------0V0-------------------------------------')
# bisect 模块
import bisect

data = [1, 4, 5, 6, 8, 12, 15, 20, 21, 23, 23, 26, 29, 30]

index_left = bisect.bisect_left(data, 20)
print(index_left)

index_right = bisect.bisect_right(data, 20)
print(index_right)

bisect.insort_left(data, 20)  # 先bisect O(logN)  再 insert O(N)
bisect.insort_right(data, 20)
print(data)

scores = [33, 99, 77, 70, 89, 90, 100, 60]


def grades(score, breakpoints=(60, 70, 80, 90), mark='FDCBA'):
    i = bisect.bisect_left(breakpoints, score)
    return mark[i]


print([grades(score) for score in scores])

# array.array 存储大量数字类型数据，可以选择 array.array 或者 numpy
# 支持所有的可变序列的特性，即列表能做的，它基本都能做
# 此外，还支持直接从文件中读取数据或者存入数据到文件

import array
import random
import time


# start = time.time()
# data = array.array('d', [random.random() for i in range(10**7)])  # 1.4262282848358154
# # data = [random.random() for i in range(10**7)]  # 1.085099458694458
# print(data[-1])
# f = open('float', 'wb')
# data.tofile(f)
# # 取
# array_data = array.array('d')
# f = open('float', 'rb')
# array_data.fromfile(f, 10**7)
# print(array_data[-1])
# print(time.time() - start)

# deque
from collections import deque

dq = deque(range(10), maxlen=10)  # 同过 maxlen 可以实现保存最近使用的数据
dq.append(10)
dq.pop()
dq.appendleft(0)
dq.extend([10, 11, 12])
dq.extendleft([-1, -2])
dq.rotate(-4)  # n > 0 将后面n个移到前面，n < 0 将前面的n个移到后面
print(dq)



























