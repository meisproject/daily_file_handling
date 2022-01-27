#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
# 提取gtf文件中的基因和GeneType对照表
import os
import re


# 提取gtf文件里的基因id和基因类型
def get_genetype(path, file):
    with open(os.path.join(path, file)) as f:
        with open(os.path.join(path, 'trans_result_tmp.txt'), 'w') as new_f:
            for line in f:
                allinfo = line.rstrip('\n').split('\t')[8]
                try:
                    g_id = re.findall(re.compile(r'gene_id \"(.*?)\";'), allinfo)
                    if len(g_id) > 0:
                        new_f.writelines(g_id[0] + '\t')
                    else:
                        new_f.writelines(' \t')
                    genetype = re.findall(re.compile(r'genetype \"(.*?)\"'), allinfo)
                    if len(genetype) > 0:
                        new_f.writelines(genetype[0] + '\t')
                    else:
                        new_f.writelines(' \t')
                except:
                    continue
                new_f.writelines('\n')


# 删除重复行
def remove_duplicate(path, file2, file1=r'trans_result_tmp.txt'):
    lines_seen = set()
    with open(os.path.join(path, file1), 'r') as input_file:
        with open(os.path.join(path, file2), 'a+') as outfile:
            for line in input_file:
                if line not in lines_seen:
                    outfile.write(line)
                    lines_seen.add(line)
    os.remove(os.path.join(path, file1))


if __name__ == "__main__":
    inpath = r'C:\Users\asus\Desktop\1'
    infile = r'ref_Gallus_gallus-5.0_top_level_modify.gtf'
    resultfile = r'final_TransResult.txt'
    get_genetype(inpath, infile)
    remove_duplicate(inpath, resultfile)
