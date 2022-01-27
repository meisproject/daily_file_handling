#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
将路径下的所有总差异表格筛选需要的FC和FDR/pvalue
"""
import os
import glob
import pandas as pd


def dif_filter(input_path, logfc_col, logfc_cutoff, pvalue_fdr_col, pvalue_fdr_cutoff):
    all_files = glob.glob(os.path.join(input_path, r'*.txt'))
    os.mkdir(os.path.join(input_path, '5.SigResult(lnFC0.25adjp0.05)'))
    # print(all_files)
    for eachfile in all_files:
        # print(f'{eachfile} operating!')
        f = pd.read_csv(eachfile, sep='\t')
        f_filter = f[(f.iloc[:, (logfc_col - 1)] > logfc_cutoff) | (f.iloc[:, (logfc_col - 1)] < -logfc_cutoff)]
        f_filter = f_filter[f_filter.iloc[:, (pvalue_fdr_col - 1)] < pvalue_fdr_cutoff]
        if len(f_filter.index) < 1:
            continue
        else:
            new_name = os.path.basename(eachfile)
            new_name = new_name.replace('.txt', '_lnFC0.25_adj.p0.05.txt')
            new_name = os.path.join(input_path, '5.SigResult(lnFC0.25adjp0.05)', new_name)
            f_filter.to_csv(new_name, sep='\t', index=False)


if __name__ == '__main__':
    my_path = r'C:\Users\asus\Desktop\1\test2'
    fc = 3
    fc_cutoff = 0.25
    pvalue_fdr = 6
    fdr_cutoff = 0.05
    dif_filter(my_path, fc, fc_cutoff, pvalue_fdr, fdr_cutoff)
