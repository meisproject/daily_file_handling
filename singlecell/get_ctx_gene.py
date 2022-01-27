#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
# 将scenic结果ctx转换为基因对的格式
import re


def convert_ctx(infile, outfile):
    gene_pair = dict()
    with open(infile) as f1:
        flag = 0
        while True:
            line = f1.readline()
            if not line:
                break
            flag += 1
            if flag > 3:
                line = line.rstrip('\n')
                tf = line.split('\t')[0]
                genes = line.split('\t')[9]
                target = re.findall("\'(.+?)\'", genes)
                if gene_pair.get(tf):
                    for tar in target:
                        gene_pair[tf].append(tar)
                else:
                    gene_pair[tf] = list(target)
            else:
                continue
    with open(outfile, "w") as f2:
        f2.writelines('TF' + '\t' + 'target' + '\n')
    for pair in gene_pair.keys():
        gene_pair[pair] = set(gene_pair[pair])
        # print("TF:" + pair)
        # print("target:" + str(gene_pair[pair]))
        for tar2 in gene_pair[pair]:
            with open(outfile, "a") as f2:
                f2.writelines(pair + '\t' + tar2 + '\n')


if __name__ == "__main__":
    # 输入文件路径
    inputfile = r'C:\Users\asus\Desktop\1\test2\All.ctx_output.tsv'
    # 输出文件路径
    outputfile = r'C:\Users\asus\Desktop\1\test2\All.ctx_output.txt'
    convert_ctx(inputfile, outputfile)
