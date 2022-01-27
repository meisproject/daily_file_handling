#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
将总细胞的summarycell表格（三列，1细胞，2类型，3样本）按照样本拆开，最终表格只保留前两列
"""
import os
import pandas as pd

all_cell = r'C:\Users\asus\Desktop\1\test2\AllSample.txt'

allcell_df = pd.read_csv(all_cell, sep='\t')

for each_sample in set(allcell_df.iloc[:, 2]):
    df_tmp = allcell_df[allcell_df.iloc[:, 2] == each_sample]
    df_tmp = df_tmp.iloc[:, 0:2]
    outname = os.path.join(r'C:\Users\asus\Desktop\1\test2', each_sample + '.txt')
    df_tmp.to_csv(outname, sep='\t', index=False)
