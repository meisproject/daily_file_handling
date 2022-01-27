#! /usr/local/bin/python3
# coding:utf-8
"""
整理scCODA用的输入表格 3.0
适用于有多个细胞或单个细胞类型，多个或单个比较
还有个bug需要修，筛选后的Statistics里有些样本全是0需要删掉，不然会sccoda报错
需要注意：
1. Condition文件中样本的顺序，将control组放在case组前面
2. 将Cluster和CellType的对照表格放入celltype文件夹，
   将Statistics表格放入statistics文件夹，
   celltype文件夹和statistics文件夹中同个细胞类型的文件名一致
"""

import os
import pandas as pd


def check_compare_file(statistics_path, celltype_path):
    """
    检查celltype和statistics中一致的组
    :param celltype_path: celltype的路径
    :param statistics_path: statistics的路径
    :return: 配对好的celltype和statistics
    """
    celltype_files = os.listdir(celltype_path)
    statistic_files = os.listdir(statistics_path)
    compared_files = []
    for each_statistic in statistic_files:
        if each_statistic in celltype_files:
            compared_files.append([os.path.join(statistics_path, each_statistic),
                                   os.path.join(celltype_path, each_statistic)])
        else:
            compared_files.append([os.path.join(statistics_path, each_statistic),
                                   ""])
    actual_groups = set(celltype_files + statistic_files)
    # print(actual_groups)
    if len(compared_files) < len(actual_groups):
        print(r'有一组或多组的名称无法对应，请检查')
    # print(compared_files)
    return compared_files


def get_sccoda_file(raw_statistic, celltype, condition, group):
    """

    :param raw_statistic: seurat的Cluster或recluster直接出的statitics表格
    :param celltype: 第一列Cluster，第二列CellType（表头必须一致）
    :param condition: 第一列Sample，第二列group
    :param group: 需要的分组
    """
    group_name = os.path.basename(raw_statistic).split('.')[0]
    # print(group_name)
    condition_df = pd.read_csv(condition, sep='\t')
    condition_df.columns = ['Sample', 'Condition']
    statistic_df = pd.read_csv(raw_statistic, sep='\t')

    # 先根据挑选的分组筛选样本
    condition_filter = condition_df[condition_df.iloc[:, 1].isin(group)]

    # 筛选Cluster的Statistics表格
    select_sample = list(condition_filter.iloc[:, 0])
    select_sample = list(set(select_sample).intersection(set(statistic_df.columns)))
    # 去除Statistics表格中全是0的列

    # 根据实际statistics表格信息再过滤一次condition的样本
    condition_filter = condition_df[condition_df.iloc[:, 0].isin(select_sample)]
    # 如果筛选后的分组都还在，则输出过滤结果
    if len(set(condition_filter.iloc[:, 1])) == len(group):
        condition_filter.to_csv(f'{group_name}_{"_".join(group)}.condition.txt', sep='\t', index=False)
        select_sample = list(condition_filter.iloc[:, 0])
        select_sample.insert(0, 'Cluster')
        statistic_filter = statistic_df.loc[:, select_sample]
        # 转置表格
        statistic_cluster = statistic_filter.T
        # 把第一个index改为Sample，不然sccoda不识别
        new_index = list(statistic_cluster.index)[1:]
        new_index.insert(0, 'Sample')
        statistic_cluster.index = new_index
        statistic_cluster.to_csv(f'{group_name}_{"_".join(group)}.ClusterStatistics.txt', sep='\t', header=False)

        # 按照celltype中的信息，合并Cluster的Statistics表格
        if celltype != "":
            celltype_df = pd.read_csv(celltype, sep='\t')
            celltype_df.columns = ['Cluster', 'CellType']
            statistic_celltype = pd.merge(celltype_df, statistic_filter).iloc[:, 1:]
            statistic_celltype = statistic_celltype.groupby('CellType').sum()
            statistic_celltype = statistic_celltype.T
            statistic_celltype.to_csv(f'{group_name}_{"_".join(group)}.CellTypeStatistics.txt', sep='\t', index_label='Sample')
    else:
        print(f"{group_name}组的{'_'.join(group)}筛选后样本为{select_sample},\n分组不足，无法输出表格")


def run_multi(statistics_path, celltype_path, condition, group):
    """
    运行多组get_sccoda_file
    :param celltype_path: celltype路径
    :param statistics_path: statistics路径
    :param condition: condition文件
    :param group: 分组信息，格式类似[['AN', 'ESCC'], ['ESCC', 'MET']]
    """
    compared_groups = check_compare_file(statistics_path, celltype_path)
    for each_groups in compared_groups:
        get_sccoda_file(each_groups[0], each_groups[1], condition, group)


if __name__ == '__main__':
    os.chdir(r'C:\Users\asus\Desktop\1\test2')
    statistic_file = 'statistics'
    celltype_file = 'celltype'
    condition_file = 'Condition.txt'
    all_groups = [['AN', 'ESCC'], ['ESCC', 'MET'], ['LYMPH', 'MET']]
    # all_groups = [['N', 'P']]
    if isinstance(all_groups[0], list):
        for group_need in all_groups:
            # get_sccoda_file(statistic_file, celltype_file, condition_file, group_need)
            run_multi(statistic_file, celltype_file, condition_file, group_need)
    else:
        # get_sccoda_file(statistic_file, celltype_file, condition_file, all_groups)
        run_multi(statistic_file, celltype_file, condition_file, all_groups)
