#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
将文件夹下的excel文件按照默认的表格格式1修改样式
这个功能已经合并到change_excel_style2里了，不需要单独使用
"""
import os
import pandas as pd
# pandas调用xlsxwriter完成格式修改


def change_style(file):
    """

    :param file: 需要套格式的xls或xlsx
    """
    df = pd.read_excel(file)
    # 以xlsxwriter重新写出xlsx
    writer = pd.ExcelWriter(file, engine='xlsxwriter')
    # 写出时删除默认的header,并留出一行，以便后续增加自定义title
    df.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False, index=False)
    worksheet = writer.sheets['Sheet1']
    # 获取表格的行和列数
    (max_row, max_col) = df.shape
    # 将表格的title保存为list
    column_settings = [{'header': column} for column in df.columns]
    # print(column_settings)
    # 创建tabel格式
    worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings,
                                                     'style': 'TableStyleLight1',
                                                     'autofilter': False})
    # 冻结窗格
    worksheet.freeze_panes(1, 1)
    # 调整列宽
    for each_column in range(0, max_col):
        column_len = max(map(lambda x: len(str(x)), df.iloc[:, each_column]))
        # 如果是title最长，直接按照常规长度计算会显示不全，因此增加两个位置
        column_len = max(column_len, (len(df.columns[each_column]) + 2))
        # print(column_len)
        if column_len < 8.38:
            # print(u'小于8.38')
            # set_column第一个参数是开始列，第二个参数是结束列，第三个是列宽
            worksheet.set_column(each_column, each_column, 8.38)
        elif column_len > 50:
            # print(u'大于50')
            worksheet.set_column(each_column, each_column, 50)
        else:
            # print(u'介于两者之间')
            worksheet.set_column(each_column, each_column, 8.38/8*int(column_len))
    # 关闭容器
    writer.save()


if __name__ == "__main__":
    my_path = r'C:\Users\asus\Desktop\1\test2'
    my_files = os.listdir(my_path)
    for my_file in my_files:
        if my_file.endswith(('.xls', '.xlsx')):
            change_style(os.path.join(my_path, my_file))
        else:
            continue
