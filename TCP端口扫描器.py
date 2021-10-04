#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/4 14:53
# @Author  : Display
# @File    : TCP端口扫描器.py
# @Software: PyCharm
'''这是一个端口全连接扫描的脚本，扫描结果会比较准确，但是比较费时间'''
from socket import *

def portScanner(host, port):
    try:
        s = socket(AF_INET, SOCK_STREAM)  # 注意参数
        s.connect((host, port))  # 注意括号 (host,port)
        print('[+] %d open' % port)
        s.close()
    except:  # 如果端口连接失败，则输出$port close
        print('[-] %d close' % port)


def main():
    setdefaulttimeout(1)
    #ports = [20, 22, 23, 80, 111, 3306]  # 定义要扫描的端口，也可以在下面定义 for p in range(1,1024):
    for p in range(1,65535):
        portScanner('192.168.31.220', p)  # 设置要扫描的主机为192.168.60.130

if __name__ == '__main__':  # “Make a script both importable and executable”
    main()  # 如果这文件中的代码被外部的python文件调用是不会被执行的
