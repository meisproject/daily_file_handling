#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
1. 获取文件的编码格式
2. 统计文件总行数，默认以utf-8读取
3. 根据文件第一行统计列数，默认以utf-8读取
"""
from itertools import (takewhile, repeat)
from chardet.universaldetector import UniversalDetector


def get_encoding(file_name):
    """

    :param file_name: 需要计算编码格式的文件
    :return: chardet计算的文件编码格式
    """
    with open(file_name, 'rb') as f:
        detector = UniversalDetector()
        buffer = 1024 * 1024
        buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
        for each_context in buf_gen:
            detector.feed(each_context)
            if detector.done:
                break
        detector.close()
        # print(f'{file_name}编码格式如下：')
        # print(detector.result)
    return detector.result['encoding']


def iter_count(file_name, encoding='utf-8'):
    """

    :param encoding: 文件编码格式
    :param file_name: 需要统计的文件
    :return: 文件行数（int）
    """
    buffer = 1024 * 1024
    with open(file_name, encoding=encoding) as f:
        buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
        # 通过计算\n的数量判断行数
        return sum(buf.count('\n') for buf in buf_gen)


def get_ncol(filename, filetype, encoding='utf-8'):
    """

    :param filetype: 文件格式（txt/tsv/csv三选一）
    :param filename: 需要计算的文件
    :param encoding: 文件的编码格式，默认utf-8
    :return: 文件的列数（以第一列进行计算）
    """
    filetypes = ['txt', 'tsv', 'csv']
    if filetype not in filetypes:
        raise ValueError(f"Invalid sim type. Expected one of: {filetypes}")
    with open(filename, encoding=encoding) as f:
        f.seek(0)
        line = f.readline()
        if filetype in ('txt', 'tsv'):
            file_ncol = len(line.split('\t'))
        elif filetype == 'csv':
            file_ncol = len(line.split(','))
    return file_ncol


if __name__ == "__main__":
    my_file = r"C:\Users\asus\Desktop\1\test2\Control1.mapping_statistics.xls"
    get_encoding(my_file)
    # print(str(iter_count(my_file)))
