#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
多线程运行，完成后气泡提醒
"""
import os
from warnings import warn
from math import ceil
import threading
from multiprocessing import Pool
from filetype_convert.txt2excel import multifile2excel
from auto_RNAseq.excel2txt import multiexcel2txt
from my_decorators.time_caculate import caculate_time
from my_decorators.complete_notice import complete_notice
# import multiprocessing
# import circbase_name_estimate.mul_process_package


def create_cut_seq(max_len, cut_len):
    """
    后续可以用于根据切分数，等分list
    :param max_len: 最终生成的list长度
    :param cut_len: list中的最大数值
    :return: 由1-cut_len的数值组成的list，长度为max_len
    """
    times = ceil(max_len/cut_len)
    new_len = list(range(1, cut_len + 1)) * times
    new_len = new_len[:max_len]
    return sorted(new_len)


class InputPath:
    """
    输入文件路径，
    可以获取files，即路径下所有文件名，
    还可以获取cut_files()，即路径下按照需求分成多份的文件名
    """
    def __init__(self, path):
        self.path = path

    @property
    def files(self):
        """

        :return: InputPath中的所有文件（包括子文件夹下的文件）
        """
        all_files = []
        for ro, di, fi in os.walk(self.path):
            for files in fi:
                all_files.append(os.path.join(ro, files))
        return all_files

    def cut_files(self, cutnum=4):
        """
        将InputPath中的所有文件按照cutnum平均切分为多个list展示
        :param cutnum:切分数
        :return:切分后的文件名，分别展示在cutnum个list中
        """
        if len(self.files) <= cutnum:
            warn(f"文件数小于{cutnum}， 不可切分")
            files_cut = [self.files]
        else:
            files_cut = [list() for _ in range(cutnum)]
            # print(files_cut)
            cut_index = create_cut_seq(len(self.files), cutnum)
            for each_index, each_file in zip(cut_index, self.files):
                files_cut[each_index-1].append(each_file)
        return files_cut


# 多线程运行
class RunThread(threading.Thread):
    """
    多线程运行自定义功能
    """
    def __init__(self, input_f, cutnum, program):
        threading.Thread.__init__(self, name=program.__name__)
        self.program = program
        self.input = input_f
        self.cutnum = cutnum

    @caculate_time
    @complete_notice
    def run(self):
        """
        自定义运行部分
        """
        cut_files = self.input.cut_files(self.cutnum)
        for i, each_file in enumerate(cut_files):
            print(f"Start {threading.current_thread().name} part {i + 1}")
            list(map(self.program, each_file))
            print(f"{threading.current_thread().name} part {i + 1} done!")


# 多进程运行
@caculate_time
@complete_notice
def pool_run(inpath, programm, cut_num=4):
    """

    :param inpath: 需要处理的文件路径
    :param programm: 需要执行的命令
    :param cut_num: 进程数
    """
    filename_cut = inpath.cut_files(cut_num)
    if len(filename_cut) < cut_num:
        cut_num_final = len(filename_cut)
    else:
        cut_num_final = cut_num
    p = Pool(cut_num_final)
    for each_pool in filename_cut:
        # apply_async的args如果需要添加参数，即使只有一个参数，也要写成元组形式，且加上末尾的逗号
        # 否则不会运行，不知道是不是bug
        p.apply_async(programm, args=(each_pool,))
        # 用get的方式获取apply_async的结果可以显示子进程的报错信息，但是运行速度会慢很多
        # result = p.apply_async(programm, args=(each_pool,))
        # result.get()
    p.close()  # 关闭进程池，不再添加新进程
    p.join()  # 等待进程池中进程完成


if __name__ == "__main__":
    # 以下4行打包exe时用，另外打包exe需要将complete_notice装饰器注释掉
    # multiprocessing.freeze_support()
    # raw_path = input(r'需要转格式的表格文件夹（子文件夹下的表格也会被处理）：')
    # run_programm = int(input(r'txt2excel请输入1，excel2txt请输入2:'))
    # my_path = InputPath(raw_path)
    my_path = InputPath(r'C:\Users\asus\Desktop\1\test2')
    # print(my_path.cut_files())
    run_programm = 1
    if run_programm == 1:
        print("执行txt转excel")
        pool_run(my_path, multifile2excel)
    elif run_programm == 2:
        print("执行excel转txt")
        pool_run(my_path, multiexcel2txt)
    else:
        warn("运行异常，run_programme只能是1或2")
    # print(my_path.cut_files())
    # 1. 线程方式（适合密集IO操作）
    # 实际测试不适合表格转化
    # from auto_RNAseq.excel2txt import xlsx2txt
    # thread = RunThread(input_f=my_path, cutnum=8, program=xlsx2txt)
    # thread.start()
    # 2. 进程方式（适合密集计算操作）
    # pool_run(my_path, multifile2excel, 6)
    # pool_run(my_path, multiexcel2txt, 6)
