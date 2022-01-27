#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
表格套格式
"""
import os
import xlwings as xw
from pywintypes import com_error
import time
# xlwings需要安装依赖包pywin32
# xlwings实际上会调用电脑中安装的excel软件（excel的版本可能会有影响）


# mapping率表格
def change_mapping_file_style(file):
    """

    :param file: xls或xlsx表格
    """
    try:
        wb = app.books.open(file)
        sht = wb.sheets[0]
        i = 1
        # 找到Chr_Distribution所在行
        while True:
            cell_value = sht.range(i, 1).value
            if cell_value == 'Chr_Distribution':
                flag_row = i
                break
            i += 1
        # print(flag_row)
        # 第一个table
        table1 = sht.tables.add(source=sht.range((2, 1), (flag_row - 4, 2)), table_style_name='TableStyleLight1')
        table1.show_autofilter = False
        # 第二个table
        max_row = sht.used_range.last_cell.row
        table2 = sht.tables.add(source=sht.range((flag_row + 1, 1), (max_row, 5)), table_style_name='TableStyleLight1')
        table2.show_autofilter = False
        # 表格宽度自适应
        sht.autofit()
        wb.save(file)
        wb.close()
    # 发生异常则跳过，这里发生的异常种类不确定，有待测试
    except com_error as my_error:
        print(f'{file}发生错误，无法操作，错误为{my_error}')


# GOPathway表格
def change_gopath_style(file):
    """

    :param file: xls或xlsx表格
    """
    try:
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
    except com_error as my_error:
        print(f'{file}发生错误，无法操作，错误为{my_error}')


# 除mapping率和GOPathway外的其他表格
def change_other_style(file):
    """

    :param file: xls或xlsx表格
    """
    # App设置中将excel打开设置为不可见，即运行代码时不会打开excel
    try:
        wb = app.books.open(file)
        sht = wb.sheets[0]
        max_row = sht.used_range.last_cell.row
        max_col = sht.used_range.last_cell.column
        # # 修改整个表格的字体为宋体
        # sht.range((1, 1), (max_row, max_col)).font.name = u'宋体'

        # 判断是否GeneStructure文件，查找第一列第5行/第11行是否分别为“ExonNCRNA”和“IntraGenic”，存在则删除这两行
        if max_row > 4 & max_row < 12:
            if sht.range(5, 1).value == 'ExonNCRNA' and sht.range(11, 1).value == 'IntraGenic':
                print(f'{file} is GeneStructure, delete row 5 and 11.')
                sht.range(11, 1).api.EntireRow.Delete()
                sht.range(5, 1).api.EntireRow.Delete()
                max_row -= 2

        # 其他表格直接按照table套格式
        table = sht.tables.add(source=sht.range((1, 1), (max_row, max_col)), table_style_name='TableStyleLight1')
        table.show_autofilter = False
        sht.autofit()
        for each_column in range(1, max_col + 1):
            if sht.range(1, each_column).column_width > 50:
                sht.range(1, each_column).column_width = 50

        # 冻结窗格
        active_window = wb.app.api.ActiveWindow
        active_window.FreezePanes = False
        active_window.SplitColumn = 0
        active_window.SplitRow = 1
        active_window.FreezePanes = True

        wb.save(file)
        wb.close()
    except com_error as my_error:
        print(f'{file}发生错误，无法操作，错误为{my_error}')


if __name__ == "__main__":
    my_path = r'F:\1.梅姗姗_第二批\206.李璐雅_人_chIP&RNAseq\李璐雅老师人RNAseq & ChIPseq项目结果交付\2.ChIP'

    # 统计一下运行时间
    start = time.time()
    # 创建excel容器
    app = xw.App(visible=False, add_book=False)
    for ro, di, fi in os.walk(my_path):
        for my_file in fi:
            if my_file.endswith(('.xlsx', '.xls')):
                my_file = os.path.join(ro, my_file)
                try:
                    wb1 = app.books.open(my_file)
                    if len(wb1.sheets) >= 3 and '_Result' in wb1.sheets[0].name:
                        wb1.close()
                        change_gopath_style(my_file)
                    elif wb1.sheets[0].range(1, 1).value == '#Mapping_Statistics':
                        wb1.close()
                        change_mapping_file_style(my_file)
                    else:
                        wb1.close()
                        change_other_style(my_file)
                except com_error as my_error1:
                    print(f'{my_file}发生错误，无法操作，错误为{my_error1}')
            else:
                continue
    app.kill()
    end = time.time()
    print(u'所有表格套格式完成，耗时 %0.2f 分钟' % ((end - start)/60))
