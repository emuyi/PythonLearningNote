# todo Dict & Set
"""
散列表：根据关键字进行数据访问的数据结构。散列表是一个稀疏数组（总有空白元素）！！！，表中的单位被称为表元，包含两部分：
键的引用，值的引用，且表元是等长的。
1、dict 以及 set 都是依赖的散列表【hash表】
   可散列数据类型：简单来讲就是不可变数据类型。如果一个对象时可散列的，那么在他的生命周期里散列值是不能变的
   并且对象内部实现__hash__方法以及__eq__方法【用来与其他键作比较】
   frozenset是可散列的。tuple要看内部元素是否都是可散列数据类型。
2、dict.pop(k) 返回值并pop键值对，如果k不存在可以设置返回值，dict.popitem() 随机pop一个键值对
3、除了最常见的字典的创建方式，还能通过
    dict(zip(iter1,iter2))
    dict([(1, 2), (3, 4)])
    字典推导式
    来创建！
4、defaultdict 接收 list、str等可调用对象作为访问不存在键时的返回值。
  setdefault(k, value) 如果 k 存在，返回 k 的值，如果 k不存在 返回 value，并新增k：value键值对。
5、当访问一个不存在的键时，会调用__missing__方法。但这个方法只是在调用__getitem__的时候被触发。像调用
   dict.get(key) or key in dict 时不会触发。【注意对于原生dict而言，UserDict并不适用】
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
9、集合中的方法：1、中缀符运算(交并补） 2、iter(set), len(set), set.add(), set.remove() 如果元素
    不存在会报key error，可以使用 set.discard()【存在的话删除，不存在也不报错】
10、python 字典取值算法流程：
    计算 search_key 的散列值，并根据散列值的一部分在散列表中查找表元，如果没有找到即找到的是空表元，抛出key error
    异常。如果找到了就比较表元中的 found_key 是否等于 search_key, 如果相等返回 value，否则【散列冲突】，拿散列值
    的另外一部分再散列表中查找，重复上述流程。
11、如果要在循环中对字典进行修改操作。最好先把要操作的数据取出来放到一个新的列表中，然后再更新原列表。
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


