# coding:utf-8
import os


# 获得文件路径和文件名
def readFilename(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files, dirs, root


def deleteFilesKeggMap(files, dirs, root):
    # 删除非keggMap结尾的文件
    for ii in files:
        if ii.endswith('.KeggMap.png'):
            continue
        else:
            print('delete:',ii)
            os.remove(os.path.join(root, ii))
    # 删除该路径下子文件夹中非keggMap结尾的文件
    for jj in dirs:
        fi, di, ro = readFilename(root + "\\" + jj)
        deleteFilesKeggMap(fi, di, ro)


# “if __name__=='__main__':” 当.py文件被直接运行时，之下的代码块将被运行；当.py文件以模块形式被导入时，之下的代码块不被运行
if __name__ == '__main__':
    # 字符串前加u表示unicode编码，防止类似于中文乱码的现象，加r表示为原始字符串，可用于规避反斜杠转义
    files, dirs, root = readFilename(r"C:\Users\asus\Desktop\1\kegg\N769-PvsN786-O.log2FC1.FDR0.05.Diff")
    deleteFilesKeggMap(files, dirs, root)
