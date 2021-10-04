#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/4 14:54
# @Author  : Display
# @File    : 有道翻译.py
# @Software: PyCharm
import urllib.request
import urllib.parse
import json
import time

while True:
    content = str(input("请输入需要翻译的内容(输入'quit!'退出):"))
    if content == 'quit!':
        print("感谢使用")
        break

    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    data = {

        'i': content,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': '15837372097486',
        'sign': '8b1c0f6b6654975dcd9f89bb92d2b446',
        'ts': '1583737209748',
        'bv': 'ec579abcd509567b8d56407a80835950',
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_CLICKBUTTION'
    }
    data = urllib.parse.urlencode(data).encode('utf-8')  # 编码

    req = urllib.request.Request(url, data)
    # 伪装
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400')

    response = urllib.request.urlopen(req)

    html = response.read().decode('utf-8')  # 解码

    # json.loads()将json字符串转发成为字典，提取数据，打印
    a = json.loads(html)
    target = a['translateResult'][0][0]['tgt']
    print(target)
    time.sleep(3)
