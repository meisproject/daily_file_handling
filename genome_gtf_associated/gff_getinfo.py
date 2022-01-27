#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
# 提取gff文件中基因id、symbol、描述（李琳售后用）
import os
import re


def get_gff_info(path, file):
    with open(os.path.join(path, file)) as f:
        with open(os.path.join(path, 'trans_result.txt'), 'w') as new_f:
            for line in f:
                new_f.writelines(line.rstrip('\n') + '\t')
                allinfo = line.rstrip('\n').split('\t')[6]
                allinfo = allinfo + ';'
                try:
                    g_id = re.findall(re.compile(r'ID=(.*?);'), allinfo)
                    if len(g_id) > 0:
                        new_f.writelines(g_id[0] + '\t')
                    else:
                        new_f.writelines(' \t')
                    parent = re.findall(re.compile(r'Parent=(.*?);'), allinfo)
                    if len(parent) > 0:
                        new_f.writelines(parent[0] + '\t')
                    else:
                        new_f.writelines(' \t')
                    symbol = re.findall(re.compile(r'symbol=(.*?);'), allinfo)
                    if len(symbol) > 0:
                        new_f.writelines(symbol[0] + '\t')
                    else:
                        new_f.writelines(' \t')
                    des = re.findall(re.compile(r'Note=(.*?);'), allinfo)
                    if len(des) > 0:
                        new_f.writelines(des[0] + '\t')
                    else:
                        des = re.findall(re.compile(r'computational_description=(.*?);'), allinfo)
                        if len(des) > 0:
                            new_f.writelines(des[0] + '\t')
                        else:
                            new_f.writelines(' \t')
                except:
                    continue
                new_f.writelines('\n')


if __name__ == "__main__":
    inpath = r'C:\Users\asus\Desktop\1'
    infile = r'result_2.txt'
    get_gff_info(inpath, infile)
