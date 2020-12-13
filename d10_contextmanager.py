# todo contextmanager
"""
1、else 子句
    a、和 if 搭配 “否则” 的意思
    b、和 for、while、try/except 搭配
        for..else.. 仅当 for 循环完毕 （没有 break，没有异常之类）执行 else 子句
        while..else.. 仅当 while 因为条件为假退出 （没有 break，没有异常） 执行 else 子句
        try..except..else.. 仅当 try 没有捕获到异常，执行 else 子句

2、上下文管理器协议：__enter__, __exit__  with 关键字是用来管理上下文管理器对象，
   如常见的 with open(a.txt) as f: 相当于 __enter__ 方法中将打开的文件返回 使用 as 赋值给变量 f
   当 with 语句块执行完毕的时候，__exit__ 执行 f.close() 操作。
3、
"""
# 文件对象是一个上下文管理器对象
f = open('test.py')
print(hasattr(f, '__enter__'))
print(hasattr(f, '__exit__'))