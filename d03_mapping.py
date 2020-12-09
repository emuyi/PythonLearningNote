# todo Dict & Set
"""
散列表：根据 key 直接访问到对应值的一种数据结构。通过散列函数计算键值的映射关系，这样访问某一个key的时候，
      可以根据这种映射关系，直接访问 value 的内存地址。所以，散列表的访问速度很快，但散列表是一个稀疏数组，相对比较占用空间。
0、可以通过判断两个文件的哈希值是否相同来判断两个文件是否相同
1、dict 以及 set 都是依赖的散列表【hash表】
   可散列数据类型：简单来讲就是不可变数据类型。如果一个对象时可散列的，那么在他的生命周期里散列值是不能变的
   并且对象内部实现__hash__方法以及__eq__方法【用来与其他键作比较】
   frozenset是可散列的。tuple要看内部元素是否都是可散列数据类型。
    d = {(1, []): 1}
    Traceback (most recent call last):
      File "<input>", line 1, in <module>
    TypeError: unhashable type: 'list'
2、dict.pop(k) 返回值并pop键值对，如果k不存在可以设置返回值，dict.popitem(last=False 第一个) 随机pop一个键值对
3、除了最常见的字典的创建方式，还能通过
    dict(zip(iter1,iter2))
    dict([(1, 2), (3, 4)])
    字典推导式
    来创建！
  setdefault(k, value) 如果 k 存在，返回 k 的值，如果 k不存在 返回 value，并新增k：value键值对。
5、当访问一个不存在的键时，会调用__missing__方法。但这个方法只是在调用__getitem__的时候被触发。像调用
   dict.get(key) or key in dict 时不会触发。简而言之, __missing__ 是专门用来处理找不到的键的。
6、 k in dict.keys(), values(), items() 都时很快的，因为返回的是一个视图对象，类似集合。
7、 内置的其他映射类型：
    1、collections.OrderedDict: 有序字典
    2、collections.ChainMap(d1, d2,..) 接受多个字典，并把这些字典增和成一个映射对象再进行操作。
    并且对ChainMap对象执行赋值操作时并不会影响到原数据。
    3、collections.Counter: 计数器。计算一个可迭代对象中元素出现的次数，并且most_common(n)方法
    可以计算 top N
    4、UserDict python版的dict，自定义dict的时候常继承它。
    5、只读映射。types.MappingProxyType 如果接收一个映射类型，会返回一个只读的映射视图，但这个视图
    是动态的，会随着原数据的变化而变化。
8、set & frozenset 集合：内部元素不可变且唯一。
    集合中的元素必须是可哈希的，但集合本身不是，frozenset是。集合可以认为是只有键的字典。
    frozen_set = frozenset(iterable)
9、集合中的方法：
    1、中缀符运算(交并补）
    print(a - b)
    print(a | b)  # 并集
    print(a & b)
    2、iter(set), len(set), set.add(), set.remove() 如果元素
    不存在会报key error，可以使用 set.discard()【存在的话删除，不存在也不报错】
    3、集合推导式
    data_set = {i for i in 'abcdeiojsodjf' if i not in 'achjs'}
10、python 字典取值算法流程：
    计算 search_key 的散列值，并根据散列值的一部分在散列表中查找表元，如果没有找到即找到的是空表元，抛出key error
    异常。如果找到了就比较表元中的 found_key 是否等于 search_key, 如果相等返回 value，否则【散列冲突】，拿散列值
    的另外一部分再散列表中查找，重复上述流程。
11、如果要在循环中对字典进行修改操作。最好先把要操作的数据取出来放到一个新的字典中，然后再更新原字典。
12、sys.argv 处理命令行执行脚本时，用来接收命令行参数，已列表的形式返回执行脚本所在的路径，参数。
13、setdefault 能够减少键查询的次数
    res = index.get(word, [])
    res.append(data)
    d[word] = res
    相当于
    d.setdefault(word, []).append(data)
    且下方比上方少一次查询操作

14、defaultdict 接收 list、str, set等可调用对象作为访问不存在键时的返回值。
    dd = defaultdict(list)

"""


# 自定义不可变字典
from collections import UserDict


class FrozenDict(UserDict):

    def __init__(self, mapping):
        self.data = mapping

    def __setitem__(self, key, value):
        raise Exception('FrozenDict do not support item assignment')

    def __getitem__(self, item):
        return self.data[item]

    def __repr__(self):
        return 'FrozenDict({})'.format(str(self.data))


# ===================================== review =====================================================
# 字典基础用法
d = {'name': 'ellen', 'age': 18, 'gender': 'female'}  # or dict(a=1, b=2)
# [] 访问值，修改值，删除值, 添加
print(d['name'])  # 一般用 .get() 方法代替
d['name'] = 'bobby'
d['hobby'] = 'music'
# 方法
'''
len/d.clear/d.copy
d.get(key, default); d.setdefault(key, default)
d.items()/d.keys()/d.values() 
d.pop(key)/d.popitem()
d.fromkeys(seq, default) 快速生成字典，但是如果 default 是 可变类型的时候要注意了！ 所以
快速生成字典还是用字典生成式比较稳妥。
    d = {}.fromkeys('abc', [])
    d['a'].append(1)
    d --> {'a': [1], 'b': [1], 'c': [1]}
'''
# 用包含 (key, value) 信息的可迭代对象来创建字典
d1 = dict([('a', 1), ('b', 2), ('c', 3)])
d2 = dict(zip(list('bac'), [2, 1, 3]))
print(d1 == d2)
# d.setdefault
if 'd' not in d1:
    d1['d'] = []
d1['d'].append('ddd')

ret = d1.get('e', [])
ret.append('eee')
d1['e'] = ret

d1.setdefault('f', []).append('fff')
print(d1)

# defaultdict
from collections import defaultdict, UserDict
dd = defaultdict(list)
dd['a'] = 1
dd['e'] = [2]
dd['e'].extend([4, 5, 6])
print(dd['e'])

# counter
from collections import Counter
s = 'sdfsdfsfsdf1safsfoijwuerownoenh1283091879834523n4nodsfjgosjdgu0q4ur0u'
counter = Counter(s)
print(counter.most_common(3))  # [('s', 8), ('f', 7), ('d', 5)]
# 集合基础用法
a = set('abcdefj')
b = set('cdajhikl')
# 运算
print(a - b)
print(a.union(b))  # 并集
print(a | b)
print(a & b)

# set.add(item)
# set.remove(item)
# set.discard(item)  item 不存在不会报keyError

d3 = dict(a=1, b=2, c=3)
for i in d3:
    d3['d'] = 4

# print(d3)
"""
Traceback (most recent call last):
  File "D:/Learning/python-learning-notes/d03_mapping.py", line 146, in <module>
    for i in d3:
RuntimeError: dictionary changed size during iteration
"""
