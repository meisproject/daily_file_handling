# coding:utf-8
import os
import re


def changename(path):
    files = os.listdir(path)
    kegglist = []
    for ii in files:
        if ii.endswith('.png'):
            jj = ii.replace(r'.KeggMap', '')
            jj = re.sub(re.compile(r'^\D+'), '', jj)  # ^\D+为开头的非数字字符
            rawfile = path + '\\' + ii
            newfile = path + '\\' + jj
            os.rename(rawfile, newfile)  # 更改KeggMap图片文件名
            pathid = jj.replace(r'.png', '')
            kegglist.append(pathid)
    return kegglist


def delete_html(path, kegglist):
    files = os.listdir(path)
    for ii in files:
        if ii.endswith('.html'):
            fn = ii.replace(r'.html', '')
            if fn not in kegglist:
                os.remove(path + '\\' + ii)


if __name__ == '__main__':
    filepath = r'C:\Users\asus\Desktop\1\kegg\N769-PvsN786-O.log2FC1.FDR0.05.Diff'
    klist = changename(filepath)
    delete_html(filepath, klist)

