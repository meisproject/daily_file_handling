#! /usr/local/bin/python3
# coding:utf-8
"""
根据Summarycell的分组信息，从表达量表格中提取每组的基因均值（也可用于提取scenic热图的数据）
Summarycell表格中必须只有两列，且第二列叫Cluster
"""

import pandas as pd
from my_decorators.time_caculate import caculate_time


@caculate_time
def get_mean(exp_dat, cell_info, result_file):
    """

    :param exp_dat: 原始表达量表格（每行是基因，每列是细胞）
    :param cell_info: 细胞和对应的分组表格，第一列是Cell，第二列是Cluster
    :param result_file: 最终输出的表格路径和名称
    """
    exp_df = pd.read_csv(exp_dat, sep='\t', index_col=0)
    cell_df = pd.read_csv(cell_info, sep='\t', index_col=0)
    cell_df.columns = ['Cluster']
    exp_df = exp_df.transpose()
    dat_combined = exp_df.merge(cell_df, left_index=True, right_index=True)
    # dat_combined.index.name = 'Cell'
    dat_mean = dat_combined.groupby(['Cluster']).mean()
    dat_mean = dat_mean.transpose()
    dat_mean.to_csv(result_file, sep='\t', index_label='Cluster')


if __name__ == "__main__":
    exp = r'C:\Users\asus\Desktop\1\test2\Cluster_sample.mean.txt'
    summarycell = r'C:\Users\asus\Desktop\1\test2\Cluster_sample.celltype.txt'
    output_file = r'C:\Users\asus\Desktop\1\test2\CellType_sample_mean.txt'
    get_mean(exp, summarycell, output_file)
