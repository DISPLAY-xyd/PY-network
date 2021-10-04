#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/4 14:49
# @Author  : Display
# @File    : TCP服务端.py
# @Software: PyCharm
import socket
import threading
import time

# 1 首先创建一个socket对象 (使用的是ipv4的地址，使用TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 2 绑定一个地址和端口
s.bind(('127.0.0.1', 9000))
# 3 监听的最大数目
s.listen(5)
print("Waiting for connection.....")
def tcplink(sock, addr):
    print("Accept new connection from %s:%s..." % addr)

    while True:
        # 接受的最大子节数
        data = sock.recv(1024)
        time.sleep(1)
        # 获得服务器返回的数据
        # 主要使用s.recv来得到 然后可能还需要使用decode()来解码
        if not data or data.decode('utf-8') == 'exit':
            break
        elif data.decode('utf-8') == 'PlayGame':
            sock.send(("玩皮呀玩，不准玩").encode('utf-8'))
        else:
            sock.send(('Hello %s 欢迎使用最屌人工助理,Small' % data.decode('utf-8')).encode('utf-8'))
        # sock.send(("Hello %s!" % data.decode('utf-8')).encode('utf-8'))
        sock.close()
        print("Connection from %s:%s closed." % addr)
        # decode('utf-8') 是使用utf-8来解析
        # encode('utf-8') 是使用utf-8来编码
    while True:
        sock, addr = s.accept()  # 获取sock和地址

        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.start()