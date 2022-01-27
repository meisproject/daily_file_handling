#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
plotnine的教程
柱状图加计数和比例
"""
from plotnine import *
from plotnine.data import mtcars


def combine(counts, percentages):
    """

    :param counts:计数
    :param percentages:比例
    :return:格式为计数加比例的字符串，如7 (14%)
    """
    fmt = '{} ({:.1f}%)'.format
    return [fmt(c, p) for c, p in zip(counts, percentages)]


(ggplot(mtcars, aes('factor(cyl)', fill='factor(cyl)'))
 + geom_bar()
 + geom_text(
            aes(label=after_stat('combine(count, prop*100)'), group=1),
            stat='count',
            nudge_y=0.125,
            va='bottom',
            size=9
        )
 + facet_wrap('am')
 ).draw(show=True)
