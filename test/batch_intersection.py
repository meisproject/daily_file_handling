#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
# 多个文件夹下的文件和同一个文件取交集（交集信息均在第一列）
# 目前需要自己手动改第一列的title为一致的
import os
import pandas as pd
from auto_RNAseq.ncRNA_mRNA_split import new_to_excel


# 获得文件路径和文件名
def read_file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files, dirs, root


def intersection(raw_file, annotations, jointype, on):
    pd.set_option('io.excel.xlsx.writer', 'openpyxl')
    f1 = pd.read_csv(raw_file, sep='\t')
    f2 = pd.read_csv(annotations, sep='\t')
    # pd.merge里有个参数on，可以自己写两个文件中需要取交集的列
    # 如果是默认状态会直接取两个表格中表头相同的列作为交集列
    if on == " ":
        overlap = pd.merge(f1, f2, how=jointype)
    else:
        overlap = pd.merge(f1, f2, how=jointype, on=on)
    newfile = os.path.splitext(raw_file)[0] + r'_anno.xlsx'
    new_to_excel(overlap, newfile)
    # with pd.ExcelWriter(newfile) as writer:
    #     overlap.to_excel(writer, index=False)


def getfile(files, dirs, root, fi2, jointype, on):
    for file in files:
        if file.endswith('.txt'):
            fi1 = os.path.join(root, file)
            intersection(fi1, fi2, jointype, on)
    for jj in dirs:
        fi, di, ro = read_file_name(root + "\\" + jj)
        getfile(fi, di, ro, fi2, jointype, on)


if __name__ == '__main__':
    f, filepath, roots = read_file_name(r"C:\Users\asus\Desktop\1\test2\新建文件夹")
    annofile = r'C:\Users\asus\Desktop\1\test2\All.counts_anno.txt'
    # how是交集方式，类似于dplyr里的left_join、inner_join等
    how = "inner"
    join_on = "AccID"
    getfile(f, filepath, roots, annofile, how, join_on)
