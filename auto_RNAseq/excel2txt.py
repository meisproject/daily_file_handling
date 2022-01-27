#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
excel转txt
"""
import os
from functools import reduce
import glob
import xlrd
from openpyxl import load_workbook
import pandas as pd
from my_decorators.time_caculate import caculate_time
# pandas新版本中读取xlsx调用的是openpyxl库，但是pandas读取文件会比openpyxl的read_only模式慢
# openpyxl读取xlsx文件，xlrd读取xls文件


# 利用pandas将路径下的所有表格转化为txt（不包括子文件夹）
@caculate_time
def excel2txt1(path):
    """
    调用pandas库进行转化

    :param path: 需要转格式的文件所在的文件夹
    """
    filelist = glob.glob(os.path.join(path, r'*.xls*'))
    for file in filelist:
        p = pd.read_excel(file, header=None)
        col_len = len(p.columns)
        row_len = len(p.index)
        with open(os.path.splitext(file)[0] + '.txt', 'w') as f:
            for row in range(0, row_len):
                for col in range(0, col_len):
                    content = p.iloc[row, col]
                    # pd.isnull是判断数值是否为nan的方法
                    # 如果为nan，则替换为""
                    if pd.isnull(content):
                        content = ""
                    if col == col_len - 1:
                        f.writelines(str(content).replace('\n', ''))
                        continue
                    f.writelines(str(content))
                    f.writelines('\t')
                f.writelines('\n')


# 利用openpyxl将路径下的所有表格转化为txt（不包括子文件夹）
@caculate_time
def excel2txt_path(path):
    """
    调用openpyxl库进行格式转化（xlsx/xls -> txt）

    :param path: 需要转格式的文件所在的文件夹
    """
    filelist = glob.glob(os.path.join(path, r'*.xls*'))
    multiexcel2txt(filelist)


# 单个表格转化为txt
def xlsx2txt(file):
    """
    调用openpyxl库进行格式转化（xlsx -> txt）

    :param file: 需要转格式的单个文件（str）
    """
    if file.endswith('xlsx'):
        wb = load_workbook(filename=file, read_only=True)
        ws = wb.active
        # 根据openpyxl的官方文档说明，read_only模式会直接获取创建excel的工具提供的表格大小信息，
        # 有些时候提供的信息有误，会导致读取不全，
        # 因此可以通过calculate_dimension()获取表格大小，如果大小明显不对，
        # 可以通过reset_dimensions()矫正
        if ws.calculate_dimension() == "A1:A1":
            ws.reset_dimensions()
        # print(f'开始处理{file}')

        with open(os.path.splitext(file)[0] + '.txt', 'w', buffering=1024) as f:
            for row in ws.rows:
                # 把每行所有值拼成一个完整的行，再按行输出
                new_row = list()
                # lambda隐式函数中如果要调用if else，会先写true的值，再写判断，最后写false的值
                # map是惰性的，需要套用list使函数运行
                list(map(lambda x: new_row.append(x.value) if x.value is not None else new_row.append(''), row))
                row_values = reduce(lambda x, y: str(x) + '\t' + str(y), new_row)
                f.write(row_values)
                f.write('\n')
        wb.close()
        print(f"{file} complete！")


def xls2txt(file):
    """
    调用xlrd库进行格式转化（xls -> txt）

    :param file: 需要转格式的单个文件（str）
    """
    if file.endswith('xls'):
        book = xlrd.open_workbook(file)
        sh = book.sheet_by_index(0)
        with open(os.path.splitext(file)[0] + '.txt', 'w', buffering=1024) as f:
            for rx in range(sh.nrows):
                for each_value in sh.row_values(rx):
                    f.write(str(each_value))
                    f.write('\t')
                f.write('\n')
        print(f"{file} complete！")


# 多个表格（list）转化为txt
def multiexcel2txt(files):
    """

    :param files: 需要处理的文件（list）
    """
    for file in files:
        if file.endswith('.xls'):
            xls2txt(file)
        elif file.endswith('.xlsx'):
            xlsx2txt(file)
        else:
            print(f'{file} is not xls/xlsx, skip')


if __name__ == "__main__":
    filedir = r'C:\Users\asus\Desktop\1\test2'
    excel2txt_path(filedir)
