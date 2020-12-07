i = iter(range(10))
# print(next(i))
# print(next(i))

# 迭代常常是隐形的。模拟 for i in xxx:


def for_simulator(iterable):
    iterator = iter(iterable)
    while True:
        try:
            print(next(iterator))
        except StopIteration:
            break


for_simulator(range(10))