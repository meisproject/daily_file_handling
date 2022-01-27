# coding:utf-8
import urllib.request  # 网页下载相关？
import re   # 正则表达式相关
from bs4 import BeautifulSoup   # 网页解码相关，需另外安装lxml
import socket
import time


def get_path(url, path):
    rawpage = urllib.request.urlopen(url)  # 打开网页
    pcontent = rawpage.read()  # 读取网页内容
    rawpage.close()  # 关闭request
    html = pcontent.decode('utf-8')  # 说明网页由utf8编码
    reg_html = re.compile('<dt>\d+</dt><dd><a href="/kegg-bin/show_pathway.+</dd>')
    html_list = reg_html.findall(html)  # 找到pathway路径行整行
    url_list = []
    f = open(path + r'\allurl.txt', 'w')
    for cont in html_list:
        map_id = re.findall(r'<dt>\d+</dt>', cont)
        map_id = map_id[0][4:-5]   # 提取mapID
        rawhref = re.findall(r'href=".+?">', cont)
        rawhref = rawhref[0][6:-2]   # 获取网页路径（href信息）
        href = r'https://www.kegg.jp' + rawhref        # 补全路径
        url_list.append(href)
        pathname = re.findall(r'">.+</a>', cont)
        pathname = pathname[0][2:-4]    # 获取通路名称
        f.writelines(map_id + '\t' + href + '\t' + pathname + '\n')
    f.close()
    return url_list


def get_anno(url_lists, path):
    socket.setdefaulttimeout(20)    # 超时无效设置？
    for urllist in url_lists:
        try:
            page = urllib.request.urlopen(urllist)
            content = page.read()
            page.close()
            soup2 = BeautifulSoup(content, features='lxml')
            area = soup2.find_all('map')
            mapline = soup2.find_all('img', src=re.compile(r'/kegg/pathway/.+'))
            pattern = re.compile(r'/kegg/pathway/\w+/\D+')  # \w是单词字符，\D是非数字
            mapname = re.sub(pattern, '', mapline[0].get('src'))  # 获取mapID
            mapname2 = mapname.replace(r'.png', '')
            file = open(path + r'\\' + mapname2 + r'.html', 'w')
            file.write(r'<img src="./' + mapname + '" name="pathwayimage" usemap="#mapdata" border="0" />\n')
            file.write('\n')
            file.write(str(area[0]))
            file.close()
        except:
            print(urllist + u'无法下载')
        time.sleep(3)  # 程序休眠3s


if __name__ == '__main__':
    inputpath = r"C:\Users\asus\Desktop\1\aaa"
    inputurl = r'https://www.kegg.jp/kegg/pathway.html'
    inputurllist = get_path(inputurl, inputpath)
    get_anno(inputurllist, inputpath)
