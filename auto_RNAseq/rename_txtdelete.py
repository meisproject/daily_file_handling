#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
批量删除文件夹及子文件夹下的txt，并将intersection改为维恩
"""
import os


# 获得文件路径和文件名
def read_file_name(file_dir):
    """

    :param file_dir: 需要处理的文件夹
    :return: 返回文件夹下的所有文件，子文件夹和文件夹绝对路径
    """
    for root, dirs, files in os.walk(file_dir):
        return files, dirs, root


# 删除txt后缀文件
def delete_txt(files, dirs, root):
    """

    :param files: read_file_name()返回的三个值分别对应这边的三个参数
    :param dirs:
    :param root:
    """
    for ii in files:
        if ii.endswith('.txt'):
            os.remove(os.path.join(root, ii))
        else:
            continue
    for jj in dirs:
        fi, di, ro = read_file_name(root + "\\" + jj)
        delete_txt(fi, di, ro)


# 维恩结果改名
def rename_intersction(dirs, root):
    """

    :param dirs: read_file_name()返回的后两个值分别对应这边的两个参数
    :param root:
    """
    try:
        os.rename(os.path.join(root, 'intersection.xls'), os.path.join(root, '维恩表.xls'))
        os.rename(os.path.join(root, 'intersection.png'), os.path.join(root, '维恩图.png'))
    except IOError:
        print(root + '文件夹下没有需要改名的文件')
    for jj in dirs:
        fi, di, ro = read_file_name(root + "\\" + jj)
        rename_intersction(di, ro)


if __name__ == '__main__':
    f, filepath, roots = read_file_name(r"C:\Users\asus\Desktop\1\test2")
    delete_txt(f, filepath, roots)
    rename_intersction(filepath, roots)
