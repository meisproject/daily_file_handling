#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
# 根据第一个表格的信息，过滤第二个表格的信息
# 第一个表格只有一列
import re


def txtfilter(file1, file2, outfile):
    need_word = list()
    with open(file1) as f1:
        while True:
            line1 = f1.readline()  # 逐行读入
            if not line1:  # 空行停止
                break
            line1 = line1.rstrip('\n')
            need_word.append(line1)
    # print(need_word)

    with open(file2) as f2:
        with open(outfile, 'a') as f3:
            final = list()
            while True:
                line2 = f2.readline()
                if not line2:
                    break
                for select in need_word:
                    if (len(re.findall(select, line2)) > 0) & (line2 not in final):
                        final.append(line2)
                    else:
                        continue
            f3.writelines(final)


if __name__ == "__main__":
    need = r'C:\Users\asus\Desktop\1\kegg_metabolism.txt'
    file_all = r'C:\Users\asus\Desktop\1\Human_KEGG_191031.gmt'
    result = r'C:\Users\asus\Desktop\1\Human_KEGG_191031_filter.gmt'
    txtfilter(need, file_all, result)
