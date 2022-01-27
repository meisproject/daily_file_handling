#! /usr/local/bin/python3
# coding:utf-8
# 将pdf转为png
# 如果pdf有多页，生成一个对应的文件夹，里面放所有的png
# 如果pdf只有一页，直接生成对应的png

import os
import glob
import ntpath
import fitz  # 使用的是PyMuPDF库


def pdf2png(pdffile):
    pdfdoc = fitz.open(pdffile)
    if pdfdoc.pageCount > 1:
        dirname = pdffile.split('.')[0]
        imagepath = os.path.join(ntpath.dirname(pdffile), dirname)
        os.makedirs(imagepath)
        for pg in range(pdfdoc.pageCount):
            page = pdfdoc.loadPage(pg)
            mat = fitz.Matrix(4, 4).preRotate(0)
            pix = page.getPixmap(matrix=mat)
            pix.writePNG(imagepath + '/' + 'images_%s.png' % pg)
    else:
        page = pdfdoc.loadPage(0)
        mat = fitz.Matrix(4, 4).preRotate(0)
        pix = page.getPixmap(matrix=mat)
        pix.writeImage(pdffile.replace('.pdf', '.png'))
    pdfdoc.close()


if __name__ == "__main__":
    # mypdfs = input(r'请将所有pdf放在一个路径下，并输入文件路径：')
    mypdfs = r'C:\Users\asus\Desktop\1\test2'
    mypdfs = glob.glob(os.path.join(mypdfs, '*.pdf'))
    for mypdf in mypdfs:
        pdf2png(mypdf)
    # input('Press Enter to exit...')
