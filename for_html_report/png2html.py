#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
# 将文件夹内的所有图片转换为报告用的多组图片html形式
import glob
import os
import ntpath
import re


def png2html(path):
    filelists = glob.glob(os.path.join(path, r'*.png*'))
    with open(os.path.join(path, 'pnghtml.html'), 'w') as f:
        flag = 1
        for filelist in filelists:
            filename = ntpath.basename(filelist)
            groupname = filename.split('.')[0]
            new_filelist = filelist.replace('\\', '/')
            new_filelist = re.sub('^.+?html', './html', new_filelist)
            # print(filelist)
            # print(new_filelist)
            # print(groupname)
            if flag == 1:
                f.writelines(r'<div class="albumSlider">' + '\n')
                f.writelines(r'	<div class="fullview">' + '\n')
                f.writelines(r'        <div class="fullview-outPrefix-label">%s</div>' % groupname + '\n')
                f.writelines(r'        <img src="%s">' % new_filelist + '\n')
                f.writelines(r'    </div>' + '\n')
                f.writelines(r'	<div class="slider">' + '\n')
                f.writelines(r'        <div class="button movebackward" title="向上滚动"></div>' + '\n')
                f.writelines(r'        <div class="imglistwrap">' + '\n')
                f.writelines(r'            <ul class="imglist">' + '\n')
            f.writelines(r'<li>' + '\n')
            f.writelines(r'     <a class="group-img-link">' + '\n')
            f.writelines(r'     <img src="%s">' % new_filelist + '\n')
            f.writelines(r'     <div class="outPrefix-label">%s</div>' % groupname + '\n')
            f.writelines(r'     </a>' + '\n' + r"</li>" + '\n')
            if flag == len(filelists):
                f.writelines(r'</ul>' + '\n' + r'</div>' + '\n')
                f.writelines(r'<div class="button moveforward" title="向下滚动"></div>' + '\n')
                f.writelines(r'</div>' + '\n')
                f.writelines(r'</div>' + '\n')
            flag = flag + 1


if __name__ == "__main__":
    filedir = r'C:\Users\asus\Desktop\1\test2'
    png2html(filedir)

