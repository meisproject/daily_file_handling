#! /usr/local/bin/python3
# coding:utf-8
"""
根据https://metacyc.org/pathway-collage-info下载的HAR文件，提取其中的pathway id和描述的关系
"""

import json
import re
from browserupproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# 使用browserupproxy的代理会打不开metacyc的网站，但别的网站可以打开，暂时不知道啥原因
def get_har_file(my_url):
    """

       :param my_url: 需要下载har文件的网址
       :return:网页中记录marker基因表格的xhr信息（链接，请求头和参数）
       """
    server = Server(r"D:\soft\browserup-proxy-1.1.0\bin\browserup-proxy.bat")
    server.start()
    my_proxy = server.create_proxy()

    # 浏览器设置
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')  # 忽略证书错误
    # 使用browserupproxy的代理会打不开metacyc的网站，但别的网站可以打开，暂时不知道啥原因
    chrome_options.add_argument('--proxy-server={0}'.format(my_proxy.proxy))  # 添加我们创建的代理
    # chrome_options.add_argument('--headless')  # 无头模式
    my_driver = webdriver.Chrome(options=chrome_options)

    # 告诉browserupproxy需要监听记录的是请求和响应
    my_proxy.new_har(options={'captureHeaders': True, 'captureContent': True})

    # 开始获取信息
    my_driver.get(my_url)
    result = my_proxy.har
    # print(result)

    # xhr_info中保存找到的url、headers和params信息
    xhr_info = []
    # 根据query string parameters 判断是否为需要的xhr信息，需要的链接一般长下面那个样子，?后面是请求的参数
    # http://bis.zju.edu.cn/MCA/data/tissues/Adrenal-Gland/
    # Adult-Adrenal-Gland/hcl_top_markers_Adult-Adrenal-Gland.json?_=1616478490635
    for entry in result['log']['entries']:
        _content = entry['response']['content']['text']
        xhr_info.append(_content)

    my_driver.close()
    my_proxy.close()
    return xhr_info


def get_from_har(infile, outfile):
    """

    :param infile: 下载的HAR文件
    :param outfile: 最终整理的文件路径及名字
    """
    with open(infile) as f:
        hardirct = json.loads(f.read())
        enterylist = hardirct['log']['entries']
        need_find = re.compile('"id":"(.+?)","label":"(.+?)"')
        all_pair = []
        for entry in enterylist:
            content = entry['response']['content']['text']
            if 'id' in content and 'label' in content:
                id_label = re.findall(need_find, content)
                for each_pair in id_label:
                    _id = each_pair[0]
                    _label = each_pair[1]
                    all_pair.append(f'{_id}\t{_label}')
        # print(list(set(all_pair)))

    with open(outfile, 'w') as f2:
        f2.writelines('ID\tLabel\n')
        for each_pair in all_pair:
            f2.writelines(each_pair + '\n')


if __name__ == "__main__":
    # print(get_har_file(r'https://metacyc.org/META/class-tree?object=Pathways'))

    har = r'C:\Users\asus\Desktop\1\test2\新建文件夹\metacyc.org.har'
    clean_dat = r'C:\Users\asus\Desktop\1\test2\新建文件夹\metacyc.txt'
    get_from_har(har, clean_dat)
