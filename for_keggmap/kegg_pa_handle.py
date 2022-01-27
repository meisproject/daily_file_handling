#! /usr/local/bin/python3
# coding:utf-8

import glob
import os
import re


def delete_href(path):
    filelist = glob.glob(os.path.join(path, r'*.txt'))  # glob类似于path.listdir，但是可以对文件进一步筛选
    for file in filelist:
        f = open(file)
        with open(file.replace('.txt', '_new.txt'), 'w') as out:
            for line in f:
                newline = re.sub('href=.+?" ', '', line)
                out.writelines(newline)
        f.close()


if __name__ == "__main__":
    file_path = r'C:\Users\asus\Desktop\1\kegg'
    delete_href(file_path)

