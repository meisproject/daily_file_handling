import os


# 列出改文件夹下的所有的txt
def select_txt(root):
    rawfiles = os.listdir(root)
    files = []
    for rawfile in rawfiles:
        if rawfile.endswith('.txt'):
            files.append(rawfile)
    print(files)
    return files


# 列出改文件夹下的所有的vcf
def select_vcf(root):
    rawfiles = os.listdir(root)
    files = []
    for rawfile in rawfiles:
        if rawfile.endswith('.vcf'):
            files.append(rawfile)
    print(files)
    return files
