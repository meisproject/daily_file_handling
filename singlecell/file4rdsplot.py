#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
根据summarycell,umiinfo和celltype文件整理单细胞按样本分组RDSplot用的表格
最终格式为第一列细胞，第二列CellType/Cluster + Sample
"""
import os

import pandas as pd


def add_celltype(paired_file, cellumiinfo):
    """

    :param paired_file: get_paired_file函数最终的结果文件，是成对的summarycell和celltype文件
    :param cellumiinfo: cellumiinfo表格名称
    """
    group_name = os.path.split(paired_file[0])[1]
    print(group_name)
    # 整理细胞和分组的对照总表
    cellumiinfo_df = pd.read_csv(cellumiinfo, sep='\t')

    # 筛选对应的cellumiinfo
    summarycell_df = pd.read_csv(paired_file[0], sep='\t')
    cluster_df = pd.merge(summarycell_df, cellumiinfo_df, left_on='Cell', right_on='CellName')
    cluster_df['Cluster_Sample'] = cluster_df['Cluster'].map(str) + '_' + cluster_df['orig.ident']
    cluster_df_output = cluster_df.sort_values(by=['Cluster', 'orig.ident'])
    cluster_df_output = cluster_df_output.loc[:, ['Cell', 'Cluster_Sample']]
    cluster_df_output.to_csv(f'{group_name}_Cluster.txt', sep='\t', index=False)

    if paired_file[1] is not None:
        celltype_df = pd.read_csv(paired_file[1], sep='\t')
        celltype_df.columns = ['Cluster', 'CellType']
        cell_celltype = pd.merge(cluster_df, celltype_df, on="Cluster")
        cell_celltype['CellType_Sample'] = cell_celltype['CellType'] + '_' + cell_celltype['orig.ident']
        cell_celltype = cell_celltype.loc[:, ['Cell', 'CellType_Sample']]
        cell_celltype = cell_celltype.sort_values(by='CellType_Sample')
        cell_celltype.to_csv(f'{group_name}_celltype.txt', sep='\t', index=False)
    else:
        print(f'{group_name}没有细胞类型信息，请注意')


def get_paired_file(summarycell_path, celltype_path):
    """

    :param summarycell_path: summarycell的文件夹路径
    :param celltype_path: cluster和celltype的对照表
    :return: 配对的summarycell表格和celltype表格
    """
    files_summarycell = os.listdir(summarycell_path)
    files_celltype = os.listdir(celltype_path)

    files_fi = []
    for each_file in files_summarycell:
        if each_file in files_celltype:
            files_fi.append([os.path.join(summarycell_path, each_file),
                             os.path.join(celltype_path, each_file)])
        else:
            files_fi.append([os.path.join(summarycell_path, each_file),
                             None])
    return files_fi


if __name__ == '__main__':
    os.chdir(r'C:\Users\asus\Desktop\1\test2')
    summarycell_dict = r'summarycell'
    celltype_dict = r'celltype'
    umiinfo = r'CellInfosFilter.txt'
    for each_pair in get_paired_file(summarycell_dict, celltype_dict):
        add_celltype(each_pair, umiinfo)
