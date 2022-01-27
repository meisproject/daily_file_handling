#! /usr/local/bin/python3
# coding:utf-8
# chipseq的PlotTss_Chromosome图片合并为一张
import os
from PIL import Image  # pillow这个包要另外装
import re


def sort_key(name):
    re_digits = re.compile(r'(chr\d+)')  # 正则外面加括号split的时候会包含匹配内容
    pieces = re_digits.split(name)
    print(pieces)
    pieces2 = re.compile(r'(\d+)').split(pieces[1])
    print(pieces2)
    logic = int(pieces2[1])
    return logic


def get_file(path):
    files = os.listdir(path)
    newfiles = []
    nfiles_int = []
    nfiles_str = []
    re_digits = re.compile(r'(chr\d+)')
    # 因为int和str不能进行比较，把chrx、chry等单独取出排序
    for file in files:
        pieces = re_digits.split(file)
        if file.endswith('.png'):
            if len(pieces) > 1:
                nfiles_int.append(file)
            else:
                nfiles_str.append(file)
    nfiles_int.sort(key=sort_key)
    nfiles_str.sort()
    newfiles.extend(nfiles_int)
    newfiles.extend(nfiles_str)
    return newfiles


def png_splice(path):
    files = get_file(path)
    num = len(files)
    fp = open(os.path.join(path, files[0]), 'rb')  # 二进制读取
    img = Image.open(fp)  # 图片不能直接关闭
    result = Image.new('RGB', (img.size[0], img.size[1]*num))
    fp.close()
    del img, fp

    flag = 0
    for file in files:
        fp = open(os.path.join(path, file), 'rb')
        img = Image.open(fp)
        result.paste(img, (0, img.size[1]*flag))
        fp.close()
        flag += 1
        del fp, img
    filename = str(files[0].split('_')[0])
    result.save(os.path.join(path, filename + r'_chrome_distribution_All.png'))


if __name__ == '__main__':
    # filepath = input(u'请输入需要合并的图片文件夹路径：')
    filepath = r'F:\1.梅姗姗_第二批\68.王新禹_人_CHIPseq\备份\4.Reads-site-Analysis'
    print(u'合并完成后窗口会自动关闭，请等待……')
    png_splice(filepath)


