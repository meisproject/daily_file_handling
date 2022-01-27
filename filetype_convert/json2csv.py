#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
将MCA数据库下载的json文件转化为csv
"""
import os
import json
import csv


def json2csv(my_file):
    """

    :param my_file: 需要转化的json文件
    """
    output_name = my_file.replace('.json', '.csv')
    if my_file.endswith('.json'):
        with open(my_file) as f1:
            rows = json.load(f1)
            print(len(rows['data']))
            with open(output_name, 'w') as f2:
                csv_write = csv.writer(f2)
                csv_write.writerow(rows['data'][0].keys())
                for row in rows['data']:
                    csv_write.writerow(row.values())


def operate_each_file(path):
    """

    :param path: 需要处理的文件所在的文件夹，对应子文件夹下的所有文件都会进行处理
    """
    for ro, di, fi in os.walk(path):
        for files in fi:
            json2csv(os.path.join(ro, files))


if __name__ == "__main__":
    my_path = r'C:\Users\asus\Desktop\1\test2'
    operate_each_file(my_path)
