#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
# 两个文件取交集或并集或差集（只支持xls、xlsx、txt）
# pandas读取xlsx调用的是xlrd库，注意xlrd库一定不能更新到2.0.0以上版本，更新后不支持xlsx读取
import os
import pandas as pd


def get_col(para):
    # 如果有多个键值，输入列数分别减1
    if isinstance(para[2], list):
        global colnum_1
        colnum_1 = list(map(lambda x: (x-1), para[2]))
    elif isinstance(para[2], int):
        colnum_1 = para[2]-1
    else:
        print('file1_col输入格式错误，请重新输入')
    if isinstance(para[3], list):
        global colnum_2
        colnum_2 = list(map(lambda x: (x-1), para[3]))
    elif isinstance(para[3], int):
        colnum_2 = para[3]-1
    else:
        print('file2_col输入格式错误，请重新输入')
    return colnum_1, colnum_2


def get_result(path, para):
    col1, col2 = get_col(para)
    # 读取文件，只支持xls、xlsx和txt三种格式
    if para[0].endswith('.xls') or para[0].endswith('.xlsx'):
        f1 = pd.read_excel(os.path.join(path, para[0]), index_col=None)
    else:
        f1 = pd.read_csv(os.path.join(path, para[0]), sep='\t')
    if para[1].endswith('.xls') or para[1].endswith('.xlsx'):
        f2 = pd.read_excel(os.path.join(path, para[1]), index_col=None)
    else:
        f2 = pd.read_csv(os.path.join(path, para[1]), sep='\t')

    # 取交集
    name1 = '_' + os.path.splitext(para[0])[0]
    name2 = '_' + os.path.splitext(para[1])[0]
    overlap = pd.merge(f1, f2,
                       left_on=list(f1.columns[col1]),
                       right_on=list(f2.columns[col2]),
                       how='inner',
                       suffixes=(name1, name2),
                       indicator=True)
    with pd.ExcelWriter(os.path.join(path, r'overlap.xlsx')) as writer:
        overlap.to_excel(writer, index=False)

    # 取并集
    union = pd.merge(f1, f2,
                     left_on=list(f1.columns[col1]),
                     right_on=list(f2.columns[col2]),
                     how='outer',
                     suffixes=(name1, name2),
                     indicator=True)
    with pd.ExcelWriter(os.path.join(path, r'union.xlsx')) as writer:
        union.to_excel(writer, index=False)


if __name__ == "__main__":
    filedir = r'C:\Users\asus\Desktop\1\test2'
    file1 = r'OPA_peaks.xlsx'
    file2 = r'OPA_peaks.peakAnno.GeneAnno.xlsx'
    # file1_col = [1]
    # file2_col = [1]
    file1_col = [1, 2, 3]
    file2_col = [1, 2, 3]
    parameter = [file1, file2, file1_col, file2_col]
    get_result(filedir, parameter)
