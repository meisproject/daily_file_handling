#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
import os

# 根据两个物种的同源基因对照表对原文件中的基因名进行替换
# 目前是将gmt中的基因名从人转成小鼠
# 同源基因对照表的第一列是现有表格中的物种基因名，第二列是需要的物种基因名
# 输出的转换后表格名字是converted.txt


def get_dict(ref):
    ref_dict = {}
    with open(ref) as f:
        while True:
            line = f.readline()  # 逐行读入
            if not line:  # 空行停止
                break
            line = line.rstrip('\n')
            raw_gene = line.split('\t')[0]
            new_gene = line.split('\t')[1]
            ref_dict[raw_gene] = new_gene
    return ref_dict


def convert_gene(rawfile, ref):
    ref_dict = get_dict(ref)
    outputfile = os.path.dirname(inputfile)
    outputfile = os.path.join(outputfile, 'converted.txt')
    with open(outputfile, 'a') as out:
        with open(rawfile) as f:
            while True:
                line = f.readline()
                line = line.rstrip('\n')
                if not line:
                    break
                for i in range(len(line.split('\t'))):
                    item = line.split('\t')[i]
                    if ref_dict.get(item):
                        item_new = ref_dict.get(item)
                    else:
                        item_new = item
                    out.writelines(item_new)
                    if i == len(line.split('\t')):
                        continue
                    else:
                        out.writelines('\t')
                out.writelines('\n')


if __name__ == "__main__":
    # inputfile是要转换基因名的表格
    inputfile = r'C:\Users\asus\Desktop\1\test2\h.all.v7.4.symbols.gmt'
    # reffile是对照表，第一列原基因，第二列需要的基因
    reffile = r'C:\Users\asus\Desktop\1\test2\human2mouse.txt'
    convert_gene(inputfile, reffile)
