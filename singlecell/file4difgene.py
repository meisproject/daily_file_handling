#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
根据summarycell,group,umiinfo和celltype文件整理单细胞差异基因用的表格
"""
import os
import pandas as pd


def add_celltype(paired_file, cellumiinfo, group_info):
    group_name = os.path.split(paired_file[0])[1]
    print(group_name)
    # 整理细胞和分组的对照总表
    cellumiinfo_df = pd.read_csv(cellumiinfo, sep='\t')
    group_df = pd.read_csv(group_info, sep='\t')
    group_df.columns = ['orig.ident', 'group']
    cell_group_all = pd.merge(cellumiinfo_df, group_df, on="orig.ident")
    cell_group_all = cell_group_all.loc[:, ['CellName', 'group']]

    # 筛选对应的cellumiinfo
    summarycell_df = pd.read_csv(paired_file[0], sep='\t')
    cells = summarycell_df['Cell'].tolist()
    cell_group_filter = cell_group_all[cell_group_all.CellName.isin(cells)]
    cell_group_filter.to_csv(f'cellumiinfo_{group_name}.txt', sep='\t', index=False)

    if paired_file[1] is not None:
        celltype_df = pd.read_csv(paired_file[1], sep='\t')
        celltype_df.columns = ['Cluster', 'CellType']
        cell_celltype = pd.merge(summarycell_df, celltype_df, on="Cluster")
        cell_celltype = cell_celltype.loc[:, ['Cell', 'CellType']]
        cell_celltype.to_csv(f'celltype_{group_name}.txt', sep='\t', index=False)
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
    sample_group = r'group.txt'
    for each_pair in get_paired_file(summarycell_dict, celltype_dict):
        add_celltype(each_pair, umiinfo, sample_group)
