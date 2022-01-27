#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
基因雷达图
"""
import matplotlib.pyplot as plt
import pandas as pd
from plotnine import *


in_file = r'C:\Users\asus\Desktop\1\test2\三组交集基因.txt'
dat_df = pd.read_csv(in_file, sep='\t')
dat_df = dat_df.iloc[:, [0, 2, 6, 10]]
# print(dat_df)

dat_df = pd.melt(dat_df, id_vars="AccID")
# print(dat_df)

plt.figure(figsize=(10, 6))  # 设置图形大小
plt.subplot(polar=True)  # 设置图形为极坐标图

# (ggplot(dat_df, aes('AccID', 'value', group='variable'))
#  # + geom_line(aes(color='factor(variable)'))
#  + geom_area(aes(color='factor(variable)',fill='factor(variable)'), alpha=.5, position=position_dodge(width=0.9))
#  + theme_void()
#  ).draw(show=True)

plt.plot(ggplot(dat_df, aes('AccID', 'value', group='variable'))
 # + geom_line(aes(color='factor(variable)'))
 + geom_area(aes(color='factor(variable)',fill='factor(variable)'), alpha=.5, position=position_dodge(width=0.9))
 + theme_void())
