# todo string 处理两方面：1、内置方法， 2、re模块
"""
1、open() 文件的时候默认是根据操作系统编码来打开文件，如果需要指定编码注意加上 encoding 参数。
2、open()、encode(), decode() 如果遇到不可编码的字符会出现 UnicodeError，这里有个errors
参数，默认是strict，即不能编解码就报错，此外还有ignore：忽略报错，但注意可能会丢数据。replace:
把不能编码的数据其他的方式替换掉。
3、能不能获取字节码的编码类型，答：不能。
"""