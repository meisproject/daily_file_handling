#! /usr/local/bin/python3
# coding:utf-8
"""
王莹项目，重新计算clonotype，如果两个细胞的链完全一致，且链对应的cdr3序列也完全一致，算一个clonotype
"""
import glob
import os

import pandas as pd


def get_clonotype(infile):
    """

    :param infile: chain filter出来的仅重链和重链加轻链文件
    """
    dat = pd.read_csv(infile, sep='\t')
    # 找出独有的cdr3序列组合
    cdr3_lists = list()
    cell_cdr3 = dict()
    all_cells = list(dat['barcode'].unique())
    for each_cell in all_cells:
        dat_cell = dat[dat['barcode'] == each_cell]
        # cdr3 = list(dat_cell.loc[:, ['cdr3_nt']]).sort()
        cdr3 = dat_cell['cdr3_nt'].values.tolist()
        cdr3 = sorted(cdr3)
        # print(cdr3)
        cell_cdr3[each_cell] = cdr3
        if cdr3 not in cdr3_lists:
            cdr3_lists.append(cdr3)
    # 每个独有的cdr3序列组合就是一个clonotype
    clonotype_list = dict()
    for cdr3_num, each_cdr3 in enumerate(cdr3_lists, 1):
        clonotype = f'clonotype{str(cdr3_num)}'
        clonotype_list[clonotype] = each_cdr3
    # 输出两个dict，看一下情况
    # dict_output(cell_cdr3, 'cell_cdr3', infile)
    # dict_output(clonotype_list, 'clonotype_list', infile)

    # 把clonotype和细胞名联系起来
    cell_clonotype = dict()
    clonotype_cell = dict()
    for each_cell in all_cells:
        cdr3_seq = cell_cdr3[each_cell]
        clonotype_name = list(clonotype_list.keys())[list(clonotype_list.values()).index(cdr3_seq)]
        # cell to clonotype，后期直接添加到原表格
        cell_clonotype[each_cell] = clonotype_name
        # clonotype to cell，后期用于计算expansion
        if clonotype_name not in clonotype_cell.keys():
            clonotype_cell[clonotype_name] = list()
            clonotype_cell[clonotype_name].append(each_cell)
        else:
            clonotype_cell[clonotype_name].append(each_cell)
    # print(cell_clonotype)
    # dict_output(cell_clonotype, 'cell_clonotype', infile)
    # 把每个细胞对应的clonotype添加到表格中
    cell_clonotype_df = pd.DataFrame.from_dict(cell_clonotype, orient='index')
    cell_clonotype_df = cell_clonotype_df.reset_index().rename(columns={'index': 'id'})
    cell_clonotype_df.columns = ['barcode', 'clonotype_new']
    dat_fi = pd.merge(dat, cell_clonotype_df, on='barcode', how='left')
    # print(cell_clonotype_df)
    # 计算每个clonotype的扩增大小，并添加到原表格
    expansion = dict()
    for each_pair in clonotype_cell.keys():
        clonotype_size = len(clonotype_cell[each_pair])
        expansion[each_pair] = clonotype_size
    # dict_output(expansion, 'expansion', infile)
    expansion_df = pd.DataFrame.from_dict(expansion, orient='index')
    expansion_df = expansion_df.reset_index().rename(columns={'index': 'id'})
    expansion_df.columns = ['clonotype_new', 'expansion_new']
    dat_fi = pd.merge(dat_fi, expansion_df, on='clonotype_new', how='left')
    result_name = infile.replace('.txt', '_new.txt')
    dat_fi.to_csv(result_name, sep='\t', index=False)


def dict_output(my_dict, group_name, raw_file):
    """
    dict转为dataframe输出表格
    :param my_dict:需要转化的dict
    :param group_name:输出表格的组名
    :param raw_file:get_clonotype中的infile（实际是为了获取文件路径）
    """
    df = pd.DataFrame.from_dict(my_dict, orient='index')
    df = df.reset_index().rename(columns={'index': 'id'})
    raw_path = os.path.dirname(raw_file)
    df.to_csv(os.path.join(raw_path, f'{group_name}.txt'), sep='\t', index=False)


if __name__ == "__main__":
    file_path = r'C:\Users\asus\Desktop\1\test2\新建文件夹'
    files = glob.glob(os.path.join(file_path, r'*.txt'))
    for each_file in files:
        get_clonotype(each_file)
    # get_clonotype(r'C:\Users\asus\Desktop\1\test2\WT_filtered_contig_annotations_both.txt')
