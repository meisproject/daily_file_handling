#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
# 根据基因表达量表格（第一列是细胞，后面的列全是各个基因的表达量）计算每个细胞的所有基因表达均值
import os
import glob


def get_exp(file_path):
    all_files = glob.glob(os.path.join(file_path, r'*.txt*'))
    for eve_file in all_files:
        eve_output = os.path.splitext(eve_file)[0] + r'_average.txt'
        # print(eve_output)
        flag = 0
        with open(eve_file) as f1:
            with open(eve_output, 'w') as f:
                while True:
                    line = f1.readline()
                    flag = flag + 1
                    if flag == 1:
                        f.writelines(r'Cell' + '\t' + 'Mean' + '\n')
                        continue
                    if not line:  # 空行停止
                        break
                    line = line.rstrip('\n')
                    line_item = line.split('\t')
                    i = 1
                    sum_num = 0
                    while i < len(line_item):
                        sum_num = sum_num + float(line_item[i])
                        i = i + 1
                    mean_num = sum_num/(len(line_item) - 1)
                    f.writelines(line_item[0] + '\t' + str(mean_num) + '\n')


if __name__ == "__main__":
    my_filepath = r'F:\1.梅姗姗_第二批\62.余山河_小鼠_单细胞（骨髓中性粒）\备份\3.5个样本分三类\7.干性和分化基因集（第三次客户给）\4.等高线图'
    get_exp(my_filepath)
