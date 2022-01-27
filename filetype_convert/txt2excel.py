#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
将文件夹下的txt、csv和tsv文件（包括假格式文件，即后缀为xlsx或xls，但实际是txt）转化为xlsx文件
行数超过500000或列数超过2000的表格都不进行操作
"""
import os
from itertools import (takewhile, repeat)

from openpyxl import Workbook


def iter_count(file_name):
    """

    :param file_name: 需要判断行数的文件
    :return:
    """
    buffer = 1024 * 1024
    with open(file_name) as f:
        buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
        return sum(buf.count('\n') for buf in buf_gen)


# 判断输入文件的格式是txt、tsv、csv、xls、xlsx还是其他
# tsv和csv只能根据后缀判断
# txt、xls还是xlsx根据二进制读取到的前6位进行区分
# 后缀是xls或xlsx的txt也可以识别
def get_file_type(in_file):
    """

    :param in_file: 单个文件
    :return: 文件类型，可以是txt、tsv、csv、xls、xlsx或other
    """
    file_name = os.path.basename(in_file)
    if in_file.endswith(('txt', 'xls', 'xlsx')):
        with open(in_file, 'rb') as bin_file:
            bin_file.seek(0)  # 回到文件头部
            title = bin_file.read(6)
            if title == b'PK\x03\x04\x14\x00':
                # print(f'{file_name} is startswith {title}, so {file_name} is xlsx.')
                return 'xlsx'
            elif title == b'\xd0\xcf\x11\xe0\xa1\xb1':
                # print(f'{file_name} is startswith {title}, so {file_name} is xls.')
                return 'xls'
            else:
                # print(f'{file_name} is startswith {title}, so {file_name} is txt.')
                if in_file.endswith(('.xls', '.xlsx')):
                    print(f'{file_name} is txt.')
                return 'txt'
    elif in_file.endswith('tsv'):
        # print(f'{file_name} is tsv.')
        return 'tsv'
    elif in_file.endswith('csv'):
        # print(f'{file_name} is csv.')
        return 'csv'
    else:
        return 'other'


# txt、tsv、csv转xlsx
def file2excel(in_file):
    """

    :param in_file: 单个文本文件
    """
    # 判断文件类型
    file_type = get_file_type(in_file)
    file_name = os.path.basename(in_file)
    # 如果是csv、txt、tsv则进行转换，否则跳过
    if file_type in ('csv', 'tsv', 'txt'):
        file_rows = iter_count(in_file)
        with open(in_file) as f1:
            f1.seek(0)
            line1 = f1.readline()
            if file_type == 'csv':
                file_cols = len(line1.split(','))
            else:
                file_cols = len(line1.split('\t'))
        # print(f'{file_name} has {file_rows} rows, {file_cols} cols.')
        # xlsx的最大行数是1048576，最大列数是16384
        # 但是为了保证转化速度，行数超过500000或列数超过2000的表格都不进行操作
        if file_rows < 500000 and file_cols < 2000:
            with open(in_file) as f:
                wb = Workbook()
                ws = wb.active
                x = 1
                while True:
                    line = f.readline()
                    if not line:
                        break
                    line = line.rstrip('\n')
                    # csv格式以逗号分隔，txt和tsv以\t分隔
                    if file_type == 'csv':
                        line_split = line.split(',')
                    else:
                        line_split = line.split('\t')
                    for i in range(len(line_split)):
                        item = line_split[i]
                        # print(type(item))
                        # 如果是有下滑线的字符串，不直接转浮点数，防止发生1_2_3这种转化为123
                        # 数值转为浮点数，防止字符串格式的数值在excel中显示有一个小绿点
                        if '_' not in item:
                            try:
                                item = float(item)
                            except ValueError:
                                pass
                        ws.cell(x, i + 1).value = item  # x单元格经度，i+1 单元格纬度，输出内容
                    x += 1
                filename = os.path.splitext(in_file)  # 将文件名和后缀拆分开
                out_file = filename[0] + ".xlsx"  # 将后缀名改为xlsx
                wb.save(out_file)  # 保存xlsx文件
            if os.path.exists(out_file) and os.path.getsize(out_file) != 0:
                os.remove(in_file)
                # print(f'{file_name} converted completed.')
            else:
                print(f'{file_name} has something wrong, please check!')
        else:
            print(f'{file_name} has {file_rows} rows, {file_cols} cols, too large, skip the file.')
    # else:
    #     print(f'{file_name} is not csv/tsv/txt, skip the file.')


def operate_each_file(path):
    """

    :param path: 需要处理的文件所在的文件夹，对应子文件夹下的所有文件都会进行处理
    """
    for ro, di, fi in os.walk(path):
        for files in fi:
            file2excel(os.path.join(ro, files))


if __name__ == "__main__":
    my_path = r'C:\Users\asus\Desktop\1\test2'
    operate_each_file(my_path)
