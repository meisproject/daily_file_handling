#! /usr/local/bin/python3
# coding:utf-8
"""
当需要整理多个细胞类型的sccoda上传文件时用这个，暂时只支持单组比较
需要注意Condition文件中样本的顺序，将control组放在case组前面
"""

import os
from warnings import warn
import pandas as pd


def check_compare_file(celltype_path, statitics_path):
    celltype_files = set(os.listdir(celltype_path))
    statics_files = set(os.listdir(statitics_path))
    union = set.union(celltype_files, statics_files)
    intersection = set.intersection(celltype_files, statics_files)
    if len(union) == len(intersection):
        print(f'需要处理的文件：{union}')
        return union
    else:
        diff_file = set.difference(union, intersection)
        warn(f'{diff_file}文件不匹配，请检查')
        print(f'需要处理的文件：{intersection}')
        return intersection


def get_sccoda_input(celltype_path, statitics_path, condition_file):
    all_files = check_compare_file(celltype_path, statitics_path)
    for each_file in all_files:
        # 读取celltype和statics两个表格，并合并
        celltype_df_name = os.path.join(celltype_path, each_file)
        statitics_df_name = os.path.join(statitics_path, each_file)
        celltype_df = pd.read_csv(celltype_df_name, sep='\t')
        celltype_df.columns = ['Cluster', 'CellType']
        statitics_df = pd.read_csv(statitics_df_name, sep='\t')
        combine_df = pd.merge(celltype_df, statitics_df, on='Cluster')
        combine_df = combine_df.groupby('CellType').sum()
        combine_df = combine_df.T
        # 根据condition中的样本顺序对合并后的statics表格排序
        condition_df = pd.read_csv(condition_file, sep='\t')
        sample_in_condition = list(condition_df.iloc[:, 0])
        sample_in_df = list(combine_df.index)
        final_sample = list()
        for each_sample in sample_in_condition:
            if each_sample in sample_in_df:
                final_sample.append(each_sample)
        combine_df = combine_df.reindex(index=final_sample)
        out_file_path = os.path.join(os.path.dirname(condition_file), each_file)
        combine_df.to_csv(out_file_path, sep='\t', index_label='Cluster')


if __name__ == '__main__':
    celltype = r'C:\Users\asus\Desktop\1\test2\celltype'
    statitic = r'C:\Users\asus\Desktop\1\test2\statistics'
    condition = r'C:\Users\asus\Desktop\1\test2\Condition.txt'
    get_sccoda_input(celltype, statitic, condition)


