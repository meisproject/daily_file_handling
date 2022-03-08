#! /usr/local/bin/python3
# coding:utf-8
"""
王莹项目，按照chain进行过滤，要求保留:
1.只有重链；
2.同时有重链和轻链
"""
import glob
import os

import pandas as pd


def filter_cell(infile):
    """
    按照要求过滤BCR的结果
    :param infile: 10X BCR cellranger的*_filtered_contig_annotations.txt表格
    """
    context = pd.read_csv(infile, sep='\t')
    all_cells = list(context['barcode'].unique())
    cells_igh = list()
    cells_both = list()
    for each_cell in all_cells:
        tmp_context = context[context['barcode'] == each_cell]
        chain = list(tmp_context['chain'].unique())
        if 'IGH' in chain:
            if len(chain) == 1:
                cells_igh.append(each_cell)
            else:
                cells_both.append(each_cell)

    # print(cells_filter)

    def filter_output(dat, group, cells, dat_name=infile):
        """
        将过滤结果输出为表格
        :param dat:
        :param group:
        :param cells:
        :param dat_name:
        """
        dat_filter = dat[dat['barcode'].isin(cells)]
        dat_name = dat_name.replace('.txt', f"_{group}.txt")
        # 计算expansion
        dat_expansion = dat_filter.loc[:, ['barcode', 'raw_clonotype_id']].drop_duplicates()
        dat_expansion = dat_expansion.groupby('raw_clonotype_id').count()
        dat_expansion.columns = ['expansion']
        # print(dat_expansion)
        dat_filter = pd.merge(dat_filter, dat_expansion, on='raw_clonotype_id')
        dat_filter.to_csv(f'{dat_name}', sep='\t', index=False)

    filter_output(context, 'igh', cells_igh)
    filter_output(context, 'both', cells_both)
    # context_igh = context[context['barcode'].isin(cells_igh)]
    # context_both = context[context['barcode'].isin(cells_both)]
    # igh_name = infile.replace('.txt', "_igh.txt")
    # both_name = infile.replace('.txt', "_both.txt")
    # context_igh.to_csv(f'{igh_name}', sep='\t', header=True, index=False)
    # context_both.to_csv(f'{both_name}', sep='\t', header=True, index=False)


if __name__ == "__main__":
    file_path = r'C:\Users\asus\Desktop\1\test2\新建文件夹'
    files = glob.glob(os.path.join(file_path, r'*.txt'))
    for each_file in files:
        filter_cell(each_file)
