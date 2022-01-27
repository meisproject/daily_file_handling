#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
# 将表格转换为报告用的html格式形式
import glob
import os
import pandas as pd


def excel2html(path, stoprow):
    filelist = glob.glob(os.path.join(path, r'*.xls*'))
    for file in filelist:
        p = pd.read_excel(file, index_col=None, header=None)
        col_len = len(p.columns)
        row_len = len(p.index)
        with open(os.path.splitext(file)[0] + '.txt', 'w') as f:
            f.writelines('<table class="pdf-table  three-wire-table dynamic-table">\n')
            f.writelines('<thead>\n')
            for row in range(0, row_len):
                f.writelines('   <tr>\n')
                if row == 0:
                    for col in range(0, col_len):
                        if col == col_len - 1:
                            f.writelines('      <th>' + str(p.iloc[row, col]).replace('\n', ''))
                            f.writelines('</th>')
                            f.writelines('\n')
                            continue
                        f.writelines('      <th>' + str(p.iloc[row, col]) + '</th>')
                        f.writelines('\n')
                    f.writelines('   </tr>')
                    f.writelines('\n')
                    f.writelines('   </thead>')
                    f.writelines('\n')
                    continue
                if row == stoprow:
                    break
                for col in range(0, col_len):
                    if col == col_len-1:
                        f.writelines('      <td>' + str(p.iloc[row, col]).replace('\n', ''))
                        f.writelines('</td>')
                        f.writelines('\n')
                        continue
                    f.writelines('      <td>' + str(p.iloc[row, col]) + '</td>')
                    f.writelines('\n')
                f.writelines('   </tr>')
                f.writelines('\n')
            f.writelines('</table>\n')


if __name__ == "__main__":
    # 表格xls或xlsx所在路径（路径下所有表格都会转成对应的html格式）
    # filedir = input(r'请输入需要转化的文件路径（格式如C:\Users\asus\Desktop\1）：')
    # myrow = int(input(r'需要转化表格前几行？'))
    filedir = r'C:\Users\asus\Desktop\1\test2\新建文件夹 (2)'
    # 表格前多少行转成html
    myrow = 7
    excel2html(filedir, myrow)
    # input('Press Enter to exit...')
