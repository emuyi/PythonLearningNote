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


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __repr__(self):
        return 'Vector({},{})'.format(self.x, self.y)


v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)