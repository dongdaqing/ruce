#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Copyright (c) 2013,掌阅科技
All rights reserved.

File Name: utils.py
Author: WangLichao
Created on: 2014-03-19
'''
import os
import time
from functools import wraps

separator = '*' * 70

class Config(dict):
    '''封装dict使之可以直接添加getattr属性
    '''
    def __getattr__(self, name):
        return self[name.lower()]

def timethis(func):
    '''修饰器用来输出函数的执行时间
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end-start)
        return result
    return wrapper

def set_color(text, color=None, on_color=None, attrs=None):
    """设置屏幕带颜色输出的属性
    Args:
        text: 输入字符串
        color: 相应颜色值int类型
            0  All attributes off 默认值
            1  Bold (or Bright) 粗体 or 高亮
            4  Underline 下划线
            5  Blink 闪烁
            7  Reverse 反显
            30 Black text
            31 Red text
            32 Green text
            33 Yellow text
            34 Blue text
            35 Purple text
            36 Cyan text
            37 White text
            40 Black background
            41 Red background
            42 Green background
            43 Yellow background
            44 Blue background
            45 Purple background
            46 Cyan background
            47 White background
        on_color: 格式化颜色输出
        attrs: 颜色属性
    """
    fmt_str = '\x1B[;%dm%s\x1B[0m'
    if color is not None:
        text = fmt_str % (color, text)
    if on_color is not None:
        text = fmt_str % (on_color, text)
    if attrs is not None:
        for attr in attrs:
            text = fmt_str % (color, text)
    return text

def print_error(msg):
    '''打印错误信息
    '''
    print set_color(msg, color=31),

def print_warning(msg):
    '''打印警告信息
    '''
    print set_color(msg, color=33),

def print_success(msg):
    '''打印成功信息
    '''
    print set_color(msg, color=32),

def tree(top):
    '''用于遍历目录
    Args:
        top: 顶级目录
    '''
    for path, names, fnames in os.walk(top):
        for fname in fnames:
            yield os.path.join(path, fname)

if __name__=='__main__':
    #test config
    with open('http_check.conf.yml') as conf_file:
        import yaml
        config = Config(yaml.load(conf_file))
        print config.http['get']['timeout']
        nimei = config.get('nime', 0)
        print nimei
    #test print with color
    print_error('error')
    print_warning('warning')
    print_success('success')
    #test tree
    files = [name for name in tree('.')]
    print files
    #test timethis
    @timethis
    def func():
        time.sleep(2)
    func()

