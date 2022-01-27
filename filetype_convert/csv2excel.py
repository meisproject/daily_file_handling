#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
import glob
import os
import pandas as pd


def csv2excel(path):
    filelist = glob.glob(os.path.join(path, r'*.csv*'))
    for file in filelist:
        p = pd.read_csv(file)
        filename = os.path.splitext(file)  # 将文件名和后缀拆分开
        with pd.ExcelWriter(os.path.join(path, filename[0] + ".xlsx")) as writer:
            p.to_excel(writer, index=False)


if __name__ == "__main__":
    filedir = input(u'请输入文件所在路径： ')
    csv2excel(filedir)

