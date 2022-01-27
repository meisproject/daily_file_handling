#! /usr/local/bin/python3
# coding:utf-8
"""
当有多组比较时，整理sccoda需要的输入文件
需要注意Condition文件中样本的顺序，将control组放在case组前面
"""

import os
import pandas as pd


def get_sccoda_file(raw_statistic, celltype, condition, group):
    """

    :param raw_statistic: seurat的Cluster或recluster直接出的statitics表格
    :param celltype: 第一列Cluster，第二列CellType（表头必须一致）
    :param condition: 第一列Sample，第二列group
    :param group: 需要的分组
    """
    condition_df = pd.read_csv(condition, sep='\t')
    statistic_df = pd.read_csv(raw_statistic, sep='\t')

    # 先根据挑选的分组筛选样本
    condition_filter = condition_df[condition_df.iloc[:, 1].isin(group)]

    # 筛选Cluster的Statistics表格
    select_sample = list(condition_filter.iloc[:, 0])
    select_sample = list(set(select_sample).intersection(set(statistic_df.columns)))
    # 根据实际statistics表格信息再过滤一次condition的样本
    condition_filter = condition_df[condition_df.iloc[:, 0].isin(select_sample)]
    # 如果筛选后的分组都还在，则输出过滤结果
    if len(set(condition_filter.iloc[:, 1])) == len(group):
        condition_filter.to_csv(f'condition_{"_".join(group)}.txt', sep='\t', index=False)
        select_sample = list(condition_filter.iloc[:, 0])
        select_sample.insert(0, 'Cluster')
        statistic_filter = statistic_df.loc[:, select_sample]
        # 转置表格
        statistic_cluster = statistic_filter.T
        # 把第一个index改为Sample，不然sccoda不识别
        new_index = list(statistic_cluster.index)[1:]
        new_index.insert(0, 'Sample')
        statistic_cluster.index = new_index
        statistic_cluster.to_csv(f'ClusterStatistics_{"_".join(group)}.txt', sep='\t', header=False)

        # 按照celltype中的信息，合并Cluster的Statistics表格
        if celltype != "":
            celltype_df = pd.read_csv(celltype, sep='\t')
            statistic_celltype = pd.merge(celltype_df, statistic_filter).iloc[:, 1:]
            statistic_celltype = statistic_celltype.groupby('CellType').sum()
            statistic_celltype = statistic_celltype.T
            statistic_celltype.to_csv(f'CellTypeStatistics_{"_".join(group)}.txt', sep='\t', index_label='Sample')
    else:
        print(f"{'_'.join(group)}筛选后样本为{select_sample},\n分组不足，无法输出表格")


if __name__ == '__main__':
    os.chdir(r'C:\Users\asus\Desktop\1\test2')
    statistic_file = 'Allsample_GraphClust.Statistics.txt'
    celltype_file = 'CellType.txt'
    condition_file = 'Condition.txt'
    all_groups = [['AN', 'ESCC'], ['ESCC', 'MET'], ['LYMPH', 'MET']]
    # all_groups = [['N', 'P']]
    if isinstance(all_groups[0], list):
        for group_need in all_groups:
            get_sccoda_file(statistic_file, celltype_file, condition_file, group_need)
    else:
        get_sccoda_file(statistic_file, celltype_file, condition_file, all_groups)
