#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
根据每月工作时间统计表计算每个项目的工作时间
"""
from dateutil import parser
from functools import reduce
import re
import xlwings as xw
from pywintypes import com_error


def time_stats(infile):
    """

    :param infile: 每月工作时间统计表
    """
    app = xw.App(visible=False, add_book=False)
    try:
        wb = app.books.open(infile)
        sht = wb.sheets[0]
        max_row = sht.used_range.last_cell.row
        max_col = sht.used_range.last_cell.column
        for each_row in range(2, max_row + 1):
            all_time = list()
            for each_col in range(8, max_col + 1):
                time_value = sht.range(each_row, each_col).value
                if time_value is not None:
                    # print(time_value)
                    time_cost = cell_time_caculate(time_value)
                    all_time.append(time_cost)
            if all_time:
                all_time_spend = reduce(lambda x, y: y + x, all_time)
                all_time_spend = str(round(int(all_time_spend.seconds) / 3600, 2))
            else:
                all_time_spend = ''
            sht.range(each_row, 7).value = str(all_time_spend)
        wb.save()
        wb.close()
    except com_error as my_error:
        print(f'{infile}发生错误，无法操作，错误为{my_error}')
    app.kill()


def cell_time_caculate(time_value):
    """

    :param time_value: 时间段，以-分割两个时间点，如9:00-10:00，如果有多个时间段，以;或；分割，如9:00-10:00;11:00-12:00
    :return: datetime.timedelta类，为time_value计算后得到的消耗时间
    """
    if ';' in time_value or '；' in time_value:
        periods = time_value.replace('\n', '')
        # 以;或；进行拆分
        periods = re.split('[;；]', periods)
        final_period = list()
        for period in periods:
            period = period.split('-')
            period = list(map(parser.parse, period))
            period = reduce(lambda x, y: y - x, period)
            final_period.append(period)
        final_period = reduce(lambda x, y: x + y, final_period)
        # print(final_period)
        return final_period
    else:
        period = time_value.split('-')
        period = list(map(parser.parse, period))
        period = reduce(lambda x, y: y - x, period)
        # print(period)
        return period


if __name__ == "__main__":
    stat_file = r'C:\Users\asus\Desktop\1\test2\工作簿1.xlsx'
    time_stats(stat_file)
