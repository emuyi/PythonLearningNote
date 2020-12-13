# todo coroutine
"""
1、gen.send(arg)
    ”send() 可以向协程发送数据，发送的数据会赋值给 yield 语句“
    send(arg) 和 next() 都可以推动生成器的执行，都能获取 yield 出来的值，不过send()可以向生成器发送值，
    next()只是从生成器获取值。
2、使用 send 发数据前要 next()或者 send(None) 预激协程。
    因为 send 发送的数据是要赋值给 yield 语句的，当协程还是未激活状态的时候，send 就无法正确的发送数据。
3、如何中止协程？
     coro.throw()/coro.close()
     都是根据协程中如果出现未处理的异常，协程会中止的原理，不过是，throw 会抛出你指定的异常类型，
     close 是抛 GeneratorExit 的异常。【如果你在协程中处理了相关的异常，那协程会继续往下执行】
     或者 send None 在协程中做中止处理
4、让协程返回值并获取返回到的值
    使用 return 返回值就可以；
    返回值的会被赋值给 StopIteration 异常的 value 属性，所以可以在外部捕获这个异常获取它的 value 属性，
    也就是返回值。
5、yield from
    1、简化 for 循环中 的 yield 表达式 即
        for i in 'ab'
            yield i     yield from 'ab'
    2、yield from 可以处理子生成器，将调用方和子生成器直接联系起来，二者可以直接进行数据交换，还可以直接传入异常。
    

"""


def gen_coroutine():
    print('start')
    x = yield 1
    print('x is %s' % x)
    print('end')


# gencor = gen_coroutine()
# value = next(gencor)
# print(value)
# gencor.send(100)
"""
start
1
x is 100
end
StopIteration
"""


def gen_coro(a):
    print('-> Started: a =', a)
    b = yield a
    print('-> Received: b =', b)
    c = yield a + b
    print('-> Received: c =', c)


# coro = gen_coro(10)
# print(next(coro))
# print(coro.send(20))  # 会 yield a + b  30
# coro.send(100)


# 协程版本的求移动平均值
def coro_avg():
    total = 0
    count = 0
    avg = 0
    while True:  # 如何中止呢？
        item = yield avg   # 赋值是在协程再次激活的时候进行的
        total += item
        count += 1
        avg = total / count


avg = coro_avg()
next(avg)
print(avg.send(10))
print(avg.send(20))
print(avg.send(30))
# 对协程进行终止
avg.close()


# 让协程返回值并获取返回值
def has_return_coro():
    total = 0
    count = 0
    avg = 0
    while True:
        item = yield
        if item is None:
            break
        total += item
        count += 1
        avg = total / count
    return avg, count


avg = has_return_coro()
next(avg)
avg.send(10)
try:
    avg.send(None)
except StopIteration as e:
    print(e.value)

