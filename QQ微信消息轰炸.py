#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/4 14:53
# @Author  : Display
# @File    : QQ微信消息轰炸.py
# @Software: PyCharm
from pynput.mouse import Button, Controller as mouse_Controller
from pynput.keyboard import Key, Controller as key_Controller
import time

time.sleep(3)
mouse = mouse_Controller()  # 控制鼠标
keyboard = key_Controller()
mouse.press(Button.left)  # 按住鼠标左键
mouse.release(Button.left)  # 松开鼠标左键
for i in range(99):
    time.sleep(0.1)
    keyboard.type('不就三杯水嘛，杜总那都是小意思啊？')
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

