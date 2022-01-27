#! /usr/local/bin/python3
# coding:utf-8
# selenium和pillow是第三方库，需要安装
# ChromeDriver需要按照chrome浏览器的版本下载对应的版本，下载后放到浏览器安装路径，并配置到环境变量

import os
from PIL import Image
from selenium import webdriver
from time import sleep
from for_html_report.all_print import fullpage_screenshot


def cut_pic(path, in_html, ne_ele):
    fullpage_screenshot(path, in_html)  # 全屏截图

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 无头模式下会有滚动条
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-infobars')
    adriver = webdriver.Chrome(chrome_options=options)
    adriver.get(in_html)

    for part in ne_ele:
        try:
            ele = adriver.find_element_by_id(part)
            ele_width = ele.size['width'] + ele.location['x']
            ele_height = ele.size['height'] + ele.location['y']
            size = (ele.location['x'], ele.location['y'], ele_width, ele_height)  # 元素位置
            print(u"元素{4}起始位置在（{0},{1}），终止位置在（{2},{3}）".format(size[0], size[1], size[2], size[3], part))
            img = Image.open(os.path.join(path, 'WholePage.png'))
            cropped = img.crop(size)
            cropped.save(os.path.join(path, part + '.png'))
            del img, cropped
            sleep(1)
        except:
            print(part + u'截图出错了')
            continue

    adriver.close()
    adriver.quit()


if __name__ == '__main__':
    filepath = r'C:\Users\asus\Desktop\1\printscreen'
    inputhtml = r'C:\Users\asus\Desktop\1\printscreen\AelaIP.html'
    element_need = ['read1_adapters', 'duplication_figure', 'insert_size_figure',
                    'plot_Before_filtering__read1__quality', 'plot_Before_filtering__read1__base_contents',
                    'Before_filtering__read1__KMER_counting']
    cut_pic(filepath, inputhtml, element_need)
