#! /usr/local/bin/python3
# coding:utf-8
"""
来源：https://blog.csdn.net/weixin_37251044/article/details/106795930
"""
from hashlib import md5
import time
import os


def calmd5(str_str):
    """

    :param str_str: 需要计算的字符串
    :return: 返回md5字符串
    """
    m = md5()
    m.update(str_str)

    return m.hexdigest()


def calmd5forfile(file):
    """

    :param file: 需要计算的文件
    :return: 返回md5字符串
    """
    start_info = os.stat(file)

    if int(start_info.st_size) / (1024 * 1024) >= 1000:
        print("File size > 1000, move to big file...")        
        return calmd5forfile(file)

    m = md5()
    f = open(file, 'rb')
    m.update(f.read())
    f.close()

    return m.hexdigest()


def calmd5forfolder(dir_dir, md5file):
    """

    :param dir_dir: 需要计算md5码的文件夹路径
    :param md5file: 计算得到的md5码文件
    """
    outfile = open(md5file, 'w')
    for root, subdirs, files in os.walk(dir_dir):
        for file in files:
            filefullpath = os.path.join(root, file)
            """print filefullpath"""

            filerelpath = os.path.relpath(filefullpath, dir_dir)
            md5_value = calmd5forfile(filefullpath)
            outfile.write(filerelpath + ' ' + md5_value + "\n")
    outfile.close()


def calmd5forbigfile(file):
    """

    :param file: 需要计算md5的大文件
    :return: 返回md5字符串
    """
    m = md5()
    f = open(file, 'rb')
    buffer = 8192  # why is 8192 | 8192 is fast than 2048

    while True:
        chunk = f.read(buffer)
        if not chunk:
            break
        m.update(chunk)

    f.close()
    return m.hexdigest()


if __name__ == "__main__":
    file_path = r'C:\Users\asus\Desktop\1\test2'
    with open(os.path.join(file_path, 'md5_allsample.txt'), 'w') as f:
        # for rt, di, fi in os.walk(file_path):
        #     for each_file in fi:
        #         file_name = os.path.join(rt, each_file)
        #         time_before = time.time()
        #         md5_value = calmd5forbigfile(file_name)
        #         print(f'文件{file_name} md5计算完成')
        #         print(f'耗时 {time.time() - time_before} 秒')
        #         f.writelines(file_name + '\t' + md5_value + '\n')
        files = os.listdir(file_path)
        for each_file in files:
            if each_file.endswith('.gz'):
                file_name = os.path.join(file_path, each_file)
                time_before = time.time()
                md5_value = calmd5forbigfile(file_name)
                print(f'文件{each_file} md5计算完成')
                print(f'耗时 {time.time() - time_before} 秒')
                f.writelines(each_file + '\t' + md5_value + '\n')
