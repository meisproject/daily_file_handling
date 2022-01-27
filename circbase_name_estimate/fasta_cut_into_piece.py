#! /usr/local/bin/python3
# coding:utf-8
import time
import math


def seq_count(fafile):
    count = 0
    start = time.time()
    with open(fafile, 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            if line.startswith(r'>'):
                count += 1
    end = time.time()
    print(u'需要注释的序列共有 %s 个，数量统计耗时 %0.2f 秒.' % (count, (end - start)))
    return count


def seq_cut(fafile):
    count = seq_count(fafile)
    datalist = []
    f_list = []
    # start = time.time()
    if count > 10000:
        new_count = math.ceil(count/4)  # 准备切分为4个
        num = 1
        with open(fafile, 'r') as file:
            flag = 0
            for line in file:
                if line.startswith(r'>'):
                    flag += 1
                    if flag == num * new_count + 1:
                        f_list.append(datalist)  # 保存前3个切分文件
                        datalist = []
                        num += 1
                datalist.append(line)
            f_list.append(datalist)  # 保存最后一个切分文件
    # end = time.time()
    # print(u'切分为4个文件，耗时 %0.2f 秒.' % (end - start))
    return f_list


def write_cutfile(path, f_list):
    filenum = 1
    # start = time.time()
    for f in f_list:
        with open(path + '\\' + str(filenum) + r'.fa', 'w') as fi:
            fi.write(''.join(f))  # ''.join()是list转str，以引号内的符号作为分割
        filenum += 1
    # end = time.time()
    # print(u'写出4个拆分后的文件，耗时 %0.2f 秒' % (end - start))


if __name__ == '__main__':
    fa = r'C:\Users\asus\Desktop\1\all.All_CircRNA.fa'
    filepath = r'C:\Users\asus\Desktop\1'
    file_list = seq_cut(fa)
    write_cutfile(filepath, file_list)

