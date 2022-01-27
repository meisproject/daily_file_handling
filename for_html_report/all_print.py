#! /usr/local/bin/python3
# coding:utf-8
import os
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# 全屏截图，来源https://www.cnblogs.com/c-x-a/p/8341141.html
# 大致原理是移动窗口将整个html分成几部分截图，然后拼在一张图上
# （如果html的长宽不是视窗的整数倍，在最边上的截图在拼接的时候会以部分重叠的方式来合并）


def fullpage_screenshot(path, in_html):
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式下会有滚动条
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-infobars')
    # chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(in_html)
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("Starting chrome full page screenshot workaround ...")

    total_width = driver.execute_script("return document.body.parentNode.scrollWidth")  # 无头模式用
    # total_width = driver.execute_script("return document.body.offsetWidth")  # 有头模式用
    total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    viewport_width = driver.execute_script("return document.body.clientWidth")
    viewport_height = driver.execute_script("return document.body.clientHeight")  # 无头模式用
    # viewport_height = driver.execute_script("return window.innerHeight")  # 无头模式用
    print("Total: ({0}, {1}), Viewport: ({2},{3})".format(total_width, total_height, viewport_width, viewport_height))
    rectangles = []

    i = 0
    while i < total_height:  # 小于文档高度时
        ii = 0
        top_height = i + viewport_height
        if top_height > total_height:  # 到最底部的时候
            top_height = total_height
        while ii < total_width:  # 小于文档宽度
            top_width = ii + viewport_width
            if top_width > total_width:  # 到最右侧的时候
                top_width = total_width
            print("Appending rectangle ({0},{1},{2},{3})".format(ii, i, top_width, top_height))
            rectangles.append((ii, i, top_width, top_height))
            # rectangle为（起始点的横坐标，起始点的纵坐标，宽度，高度）
            ii = ii + viewport_width
        i = i + viewport_height

    stitched_image = Image.new('RGB', (total_width, total_height))  # 以文档的长宽新建图片
    previous = None
    part = 0

    for rectangle in rectangles:
        if previous is not None:  # 除第一张
            driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))  # 窗口移到起始位置
            print("Scrolled To ({0},{1})".format(rectangle[0], rectangle[1]))
            time.sleep(0.2)  # 休眠0.2秒
        file_name = "part_{0}.png".format(part)
        print("Capturing {0} ...".format(file_name))
        driver.get_screenshot_as_file(file_name)  # 当前页面截图
        screenshot = Image.open(file_name)  # 打开截图

        if rectangle[1] + viewport_height > total_height:  # 如果文档高度不是视图高度的整数倍，调整最后一个图起始点的信息
            offset1 = (rectangle[0], total_height - viewport_height)
        else:
            offset1 = (rectangle[0], rectangle[1])
        if offset1[0] + viewport_width > total_width:  # 如果文档高度不是视图宽度的整数倍，调整最后一个图起始点的信息
            offset2 = (total_width - viewport_width, offset1[1])
        else:
            offset2 = (offset1[0], offset1[1])

        print("Adding to stitched image with offset ({0}, {1})".format(offset2[0], offset2[1]))
        stitched_image.paste(screenshot, offset2)  # 按照调整后的位置在长图对应位置粘贴小图
        del screenshot
        os.remove(file_name)  # 删除小图截图
        part = part + 1
        previous = rectangle

    stitched_image.save(os.path.join(path, 'WholePage.png'))  # 保存最终的长图
    driver.close()
    driver.quit()
    print("Finishing chrome full page screenshot workaround...")
    return True


if __name__ == '__main__':
    filepath = r'C:\Users\asus\Desktop\1\printscreen'
    inputhtml = r'C:\Users\asus\Desktop\1\printscreen\AelaIP.html'
    fullpage_screenshot(filepath, inputhtml)
