#! /usr/local/bin/python3
# coding:utf-8
"""
从http://bis.zju.edu.cn/MCA/index.html网站下载marker的信息
MCA数据局采用的是异步加载，数据信息存储在network的xhr信息中
参考网址1：https://blog.csdn.net/weixin_39956353/article/details/111299280
参考网址2：https://blog.csdn.net/weixin_44755148/article/details/94557870
"""
# 原来使用的是browsermobproxy，但是用这个的时候发现有些请求网址没有被获取，更换browserupproxy才可以获取
# 使用browserupproxy需要安装browserupproxy的python包，网址：https://github.com/browserup/browserup-proxy-py
# 还需要去github下载对应的文件，github地址：https://github.com.cnpmjs.org/browserup/browserup-proxy
# 注意，下载的browserup-proxy必须是1.1.0版本，尝试了2.1.0版本会报错
# 需要提前配置好chrome webdriver
import os
import re
import time
import requests
from browserupproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from simplejson.errors import JSONDecodeError


# 根据输入的MCA网页链接，找到对应的xhr信息并返回
def get_xhr_info(my_url, proxy, driver):
    """

    :param my_url: MCA数据中每个组织的gallery页面网页链接，
                   如http://bis.zju.edu.cn/MCA/gallery.html?tissue=Adult-Adrenal-Gland
    :param proxy: 由broswerupproxy开启的代理
    :param driver: 开启的webdriver
    :return:网页中记录marker基因表格的xhr信息（链接，请求头和参数）
    """
    # 告诉browserupproxy需要监听记录的是请求和响应
    proxy.new_har(options={'captureHeaders': True, 'captureContent': True})

    # 开始获取信息
    driver.get(my_url)
    result = proxy.har
    # print(result)

    # xhr_info中保存找到的url、headers和params信息
    xhr_info = dict()
    # 根据query string parameters 判断是否为需要的xhr信息，需要的链接一般长下面那个样子，?后面是请求的参数
    # http://bis.zju.edu.cn/MCA/data/tissues/Adrenal-Gland/
    # Adult-Adrenal-Gland/hcl_top_markers_Adult-Adrenal-Gland.json?_=1616478490635
    for entry in result['log']['entries']:
        _url = entry['request']['url']
        _headers = entry['request']['headers']
        _params = entry['request']['queryString']
        if len(_params) > 0:
            if _params[0]['name'] == '_':
                xhr_info['url'] = _url
                xhr_info['headers'] = _headers
                xhr_info['params'] = _params

    return xhr_info


def xhr_list2dict(xhr_list):
    """

    :param xhr_list: get_xhr_info()获取到的xhr list
    :return: 将list格式的xhr信息转化为dict格式，方便后期request获取
    """
    xhr_dict = dict()
    for each_ele in xhr_list:
        name = each_ele['name']
        value = each_ele['value']
        xhr_dict[name] = value
    return xhr_dict


def get_marker_table(my_html, output_path, proxy, driver):
    """

    :param my_html: 需要下载marker表格的网页链接
    :param output_path: 保存输出的marker表格路径
    :param proxy: 由broswerupproxy开启的代理
    :param driver: 开启的webdriver
    """
    xhr_infos = get_xhr_info(my_html, proxy, driver)
    url = xhr_infos['url']
    headers = xhr_list2dict(xhr_infos['headers'])
    params = xhr_list2dict(xhr_infos['params'])

    marker_table = requests.get(url, headers=headers, params=params)  # 调用get方法，下载marker表格
    try:
        json_marker = marker_table.json()  # 使用json()方法，将response对象，转为列表/字典
        list_marker = json_marker['data']
        # print(list_comment)
        with open(output_path, 'w') as f:
            f.writelines('p_value\tavg_diff\tpct_1\tpct_2\tcluster\tgene\talias\n')
            for gc in list_marker:
                try:
                    f.writelines(str(gc['p_val']) + '\t' + str(gc['avg_diff']) + '\t' + str(gc['pct_1']) + '\t' +
                                 str(gc['pct_2']) + '\t' + str(gc['cluster']) + '\t' + str(gc['gene']) + '\t' +
                                 str(gc['alias']) + '\n')
                except UnicodeEncodeError as my_error1:
                    print(f'无法输出，错误为：{my_error1}')
        print(f'{my_html} 数据下载完成！')
    except JSONDecodeError as my_error2:
        print(f'{my_html}下载发生错误，错误信息为{my_error2}')


def get_all_tissue():
    """

    :return: 返回MCA数据库记载的所有小鼠组织类型名字
    """
    # url是MCA的gallery页面中的记录了所有组织信息的network信息
    url = r'http://bis.zju.edu.cn/MCA/assets/js/tissueinfo-2020.js'
    headers = {
        'DNT': '1',
        'Referer': 'http://bis.zju.edu.cn/MCA/gallery.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
    }
    tissue_table = requests.get(url, headers=headers)
    txt_tissue = tissue_table.text
    # print(txt_tissue)
    all_tissues = list()
    for line in txt_tissue.split('\n'):
        # 通过正则匹配找到所有组织的名字
        tissue_info = re.findall('\"(.+?)\" :', line)
        if len(tissue_info) == 1:
            all_tissues.append(tissue_info[0])

    return all_tissues


if __name__ == "__main__":
    file_path = r'C:\Users\asus\Desktop\1\test2'
    tissues = get_all_tissue()
    # 开启代理
    server = Server(r"D:\soft\browserup-proxy-1.1.0\bin\browserup-proxy.bat")
    server.start()
    my_proxy = server.create_proxy()

    # 浏览器设置
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')  # 忽略证书错误
    chrome_options.add_argument('--proxy-server={0}'.format(my_proxy.proxy))  # 添加我们创建的代理
    chrome_options.add_argument('--headless')  # 无头模式
    my_driver = webdriver.Chrome(options=chrome_options)

    # 开始循环下载每个组织的marker基因
    for each_tissue in tissues:
        html_to_extract = r'http://bis.zju.edu.cn/MCA/gallery.html?tissue=' + each_tissue
        out_file = os.path.join(file_path, each_tissue + '.txt')
        print(f'正在下载{html_to_extract}')
        get_marker_table(html_to_extract, out_file, my_proxy, my_driver)
        time.sleep(3)  # 程序休眠3s
    # i = 1
    # for each_tissue in tissues:
    #     if i >= 121:
    #         html_to_extract = r'http://bis.zju.edu.cn/MCA/gallery.html?tissue=' + each_tissue
    #         out_file = os.path.join(file_path, each_tissue + '.txt')
    #         print(f'正在下载{html_to_extract}')
    #         get_marker_table(html_to_extract, out_file, my_proxy, my_driver)
    #         time.sleep(3)  # 程序休眠3s
    #     i += 1

    my_proxy.close()
    server.stop()
    my_driver.quit()
