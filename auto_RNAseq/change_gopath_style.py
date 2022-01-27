#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
GOPathway表格套格式
这个功能已经合并到change_excel_style2里了，不需要单独使用
"""
import os
import xlwings as xw
# xlwings需要安装依赖包pywin32
# xlwings实际上会调用电脑中安装的excel软件


def change_gopath_style(file):
    """

    :param file: 需要套格式的GOPathway结果
    """
    # App设置中将excel打开设置为不可见，即运行代码时不会打开excel
    app = xw.App(visible=False, add_book=False)
    wb = app.books.open(file)
    for each_sheet in wb.sheets:
        sht = wb.sheets[each_sheet]
        # autofit()自动调整高宽
        sht.autofit()
        # used_range是表格中已经使用的range
        info = sht.used_range
        column_num = info.last_cell.column
        for each_column in range(0, column_num):
            # print(each_column)
            # print(sht.range(1, each_column + 1).column_width)
            if sht.range(1, each_column + 1).column_width > 50:
                sht.range(1, each_column + 1).column_width = 50
    wb.save(file)
    wb.close()
    app.quit()
    pass


if __name__ == "__main__":
    my_path = r'C:\Users\asus\Desktop\1\test2'
    my_files = os.listdir(my_path)
    for my_file in my_files:
        if my_file.endswith('.xlsx'):
            change_gopath_style(os.path.join(my_path, my_file))
        else:
            continue
