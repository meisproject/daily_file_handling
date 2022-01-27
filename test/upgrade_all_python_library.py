#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
批量更新所有python第三方库，貌似不好使……
来源：https://blog.csdn.net/LC1356/article/details/105186925/
"""
import os


if __name__ == '__main__':	 # 个人习惯，可以直接把这行去了，后面所有代码逆向缩进一个tab制表符
    os.system("python -m pip install --upgrade pip")  # 更新 pip
    pyListData = os.popen("pip list --outdated")  # 比较耗时间，如果安装的库比较多，时间可能较久
    pyListData = pyListData.read()	 # 返回的字符串
    print(pyListData)
    pyList = pyListData.splitlines()	 # 解析拆分成列表
    for py in pyList[2:]:  # 遍历更新，从 2 开始是因为 第一行显示列名称，第二行显示分隔线，可以看控制台打印信息
        os.system("pip install --upgrade "+py.split(" ")[0])  # 更新库
