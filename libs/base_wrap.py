#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz

# 通用装饰器
import signal
import time
from  threading import Thread


# 信号只能在 linux 系统上 使用 在windows 上无法使用
# windows 还需要改成线程

def set_timeout(num, callback):
    def wrap(func):
        def handle(signum, frame):
            raise RuntimeError

        def to_do(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handle)
                signal.alarm(num)  # 设置 num 秒的闹钟
                r = func(*args, **kwargs)
                signal.alarm(0)  # 关闭闹钟
                return r
            except RuntimeError as e:
                print("runtime error")
                callback()

        return to_do

    return wrap


# 定义一个可获取到结果的线程
class Result_Thread(Thread):
    def __init__(self, target, args):
        Thread.__init__(self)
        self.target = target
        self.args = args

    def run(self):
        self.result = self.target(*self.args)

    def get_result(self):
        return self.result
