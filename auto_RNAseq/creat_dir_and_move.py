#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
将文件夹下所有文件按照组名新建子文件夹并将文件移动到对应的子文件夹下
组名是根据第一个.前面的内容判断的
"""
import os
import numpy as np
import shutil


# 列出文件夹下所有的文件，不包括子文件夹
def list_all_file(path):
    """

    :param path: 需要列出所有文件名的文件夹
    :return:
    """
    file_list = os.listdir(path)
    file_list_final = list()
    for each_file in file_list:
        if os.path.isfile(os.path.join(path, each_file)):
            file_list_final.append(each_file)
    # print(file_list_final)
    return file_list_final


def createdir_and_move(path):
    """

    :param path: 需要进行处理的文件夹（不能对子文件夹处理）
    """
    file_list = list_all_file(path)
    group_name = map(lambda x: x.split('.')[0], file_list)
    group_name = set(list(group_name))
    for each_group in group_name:
        file_num = np.sum(list(map(lambda x: x.startswith(each_group), file_list)))
        # print(file_num)
        if file_num > 1:
            new_dir = os.path.join(path, each_group)
            os.makedirs(new_dir)
            for each_file in file_list:
                if each_file.startswith(each_group):
                    shutil.move(os.path.join(path, each_file), new_dir)


if __name__ == "__main__":
    my_path = r'C:\Users\asus\Desktop\1\test2'
    createdir_and_move(my_path)
