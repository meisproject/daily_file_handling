#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
将文件夹下行数超过500000的txt文件拆分为多个
"""
import os
from math import ceil
import linecache
from filetype_convert.txt2excel import iter_count


def bigfilecut(file):
    """

    :param file: txt文件
    """
    line_counts = iter_count(file)
    cut_num = ceil(line_counts / 500000)
    title = linecache.getline(file, 1)
    if cut_num > 1:
        for file_num in range(1, cut_num + 1):
            file_name = file.replace('.txt', '_part' + str(file_num) + '.txt')
            with open(file_name, 'w') as f:
                f.writelines(title)

        with open(file) as raw_file:
            flag = 1
            while True:
                line = raw_file.readline()
                if not line:
                    break
                if flag != 1:
                    flag_file = ceil(flag / 500000)
                    # print(flag)
                    # print(flag_file)
                    output_file = file.replace('.txt', '_part' + str(flag_file) + '.txt')
                    with open(output_file, 'a') as f:
                        f.writelines(line)
                flag += 1


if __name__ == "__main__":
    my_path = r'C:\Users\asus\Desktop\1\test2'
    all_files = os.listdir(my_path)
    os.chdir(my_path)
    for each_file in all_files:
        if each_file.endswith('txt'):
            bigfilecut(each_file)
