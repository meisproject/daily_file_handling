#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
# 2列的txt转换成gmt格式（原始txt第一列是条目，第二列是基因）
import re


def txt2dict(file):
    flag = 0
    term_dict = dict()
    with open(file) as f:
        while True:
            flag = flag + 1
            line = f.readline()  # 逐行读入
            if not line:  # 空行停止
                break
            if flag == 1:
                continue
            else:
                line = line.rstrip('\n')
                term_name = line.split('\t')[0]
                gene = line.split('\t')[1]
                if term_dict.get(term_name):
                    term_dict[term_name].append(gene)
                else:
                    term_dict[term_name] = [gene]
    return term_dict


def dict2gmt(file):
    outname = re.sub('.txt', '.gmt', file)
    term_dict = txt2dict(file)
    with open(outname, 'w') as f2:
        for term_name in term_dict.keys():
            f2.writelines(term_name + '\t' + 'NA' + '\t')
            # join能以特定符号连接字符串
            f2.writelines("\t".join(str(i) for i in term_dict[term_name]))
            f2.writelines('\n')


if __name__ == "__main__":
    inputfile = r'C:\Users\asus\Desktop\1\test2\工作簿1.txt'
    dict2gmt(inputfile)
