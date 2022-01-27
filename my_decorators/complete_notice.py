#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
程序完成时气泡提醒的修饰器
"""


from functools import wraps
from plyer import notification


def complete_notice(func):
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
        result = func(*args, **kwargs)
        notification.notify(title='完成提醒',
                            message=f'{func.__name__}运行完成',
                            timeout=3)
        return result
    return wrapper

