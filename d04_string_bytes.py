# todo string 处理有两点：1、内置方法， 2、re模块
"""
1、open() 文件的时候默认是根据操作系统编码【win:gbk, linux/mac:utf-8】来打开文件，如果需要
指定编码注意加上 encoding 参数。
2、open()、encode(), decode() 如果遇到不可编码的字符会出现 UnicodeError，这里有个errors
参数，默认是strict，即不能编解码就报错，此外还有ignore：忽略报错，但注意可能会丢数据。replace:
把不能编码的数据其他的方式替换掉。
3、能不能获取字节码的编码类型，答：不能，除非声明的有编码类型。
！！chardet：根据编码规则做的检测包。
4、b'\xef\xb\xbf' 如果文件以这三个字节开头，有可能是带有 BOM 的utf-8文件。但是python并不会这样认为。
5、处理文本的最佳方式 —— 三明治原则。读文件的时候先解码，逻辑处理的是纯字符串，处理好了再编码。
6、不要用二进制模式打开文本文件，二进制模式用来处理二进制文件。
7、string
    序列的特性，切片，拼接，增量操作
    char.join(seq) seq 中的 item 得是str
    str.split(maxsplit=)/rsplit()
    str.find(substring)/index
    str.strip(char)
    str.count()
    str.isalnum/islower()/isupper/isdigit/isalpha
    str.startswith/endswith/lower/upper
    str.format
    str.replace(old, new)

"""
