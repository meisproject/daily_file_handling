# coding:utf-8
# 纵向合并文件，输出文件为txt
import os


def catfile2(fdir):
    filenames = os.listdir(fdir)
    f = open(fdir + '\\All.txt', 'w')
    for filename in filenames:
        if filename.endswith('.txt'):
            filepath = fdir + '\\' + filename
            for line in open(filepath):
                line = line.split('\n')[0]
                f.writelines(line + '\t' + filename + '\n')
    f.close()


if __name__ == "__main__":
    filedir = r'C:\Users\asus\Desktop\1\test2'
    catfile2(filedir)
