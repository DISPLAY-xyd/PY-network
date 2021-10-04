#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/4 14:51
# @Author  : Display
# @File    : TCP客户端.py
# @Software: PyCharm
import socket

target_host = "172.17.129.6"    #目标地址
target_port = 5542   	#目标端口号

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((target_host,target_port))

str = "啦啦啦啦啦"    #发送字符串
str = str.encode()

client.send(str)
response = client.recv(4096)
response = response.decode()
print(response)