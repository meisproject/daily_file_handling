#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
计算程序总耗时的修饰器
"""


import time
from functools import wraps


def caculate_time(func):
    """

    :param func: 被装饰的函数
    :return: 装饰器函数？
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        """

        :param args: 被装饰函数的所有位置参数
        :param kwargs: 被装饰函数的所有关键字函数
        :return: 被装饰函数的运行结果
        """
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        time_spend = round((end - start)/60, 2)
        if time_spend > 1:
            print(f"{func.__name__}执行完成， 耗时{time_spend}分钟")
        else:
            print(f"{func.__name__}执行完成， 耗时{round((end-start), 3)}秒")
        return result
    return wrapper

