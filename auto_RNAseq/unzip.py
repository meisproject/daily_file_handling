#! /usr/local/bin/python3
# coding:utf-8
"""
批量解压文件夹下的所有压缩包（包括子文件夹），并删除压缩包
"""
import zipfile
import os
from my_decorators.time_caculate import caculate_time


def read_file_name(file_dir):
    """

    :param file_dir: 需要处理的文件夹路径
    :return: 文件夹下的文件、子文件夹和文件夹的绝对路径
    """
    for root, dirs, files in os.walk(file_dir):
        return files, dirs, root


# 这边加装饰器会有问题
# @caculate_time
def unzip(files, dirs, root):
    """

    :param files: read_file_name()返回的三个值分别对应这边的三个参数
    :param dirs:
    :param root:
    """
    for file_name in files:
        if file_name.endswith('.zip'):
            file_zip = zipfile.ZipFile(os.path.join(root, file_name))
            file_zip.extractall(root)
            file_zip.close()
            os.remove(os.path.join(root, file_name))

    for jj in dirs:
        fis, dis, ros = read_file_name(root + "\\" + jj)
        unzip(fis, dis, ros)


if __name__ == "__main__":
    file_path = r'F:\1.梅姗姗_第二批\206.李璐雅_人_chIP&RNAseq\备份'
    fi, di, ro = read_file_name(file_path)
    unzip(fi, di, ro)
