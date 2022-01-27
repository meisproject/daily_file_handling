#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
doi:10.1038/s41591-019-0750-6中的Figure 1d
"""
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from scipy.stats import stats

# 需要修改的地方
# 输入的整理后表格
input_file = r'C:\Users\asus\Desktop\1\test2\Forboxplot\PDL1.txt'
# 输出路径
figure_label = r'C:\Users\asus\Desktop\1\test2\Forboxplot\PDL1'
# boxplot配色
palette = {
    'PDL1_Low': '#000000',
    'PDL1_High': '#FF0000'
}
# 散点配色
dot_palette = {
    'PDL1_Low': '#606060',
    'PDL1_High': '#FF0000'
}
# CellType顺序
labels = ['Astrocyte', 'B_Cell', 'DC', 'Endothelial', 'Epithelial', 'Fibroblast', 'Macrophage', 'Mast',
          'Microglia', 'Monocytic', 'Neutrophil', 'NKT', 'Oligodendrocyte', 'OPC', 'Plasma', 'T'
]
# 分组顺序
group_order = ['PDL1_Low', 'PDL1_High']
# 图片宽度
pic_width = 15
# 图片高度
pic_height = 6

# 以下都不要改动，画图
tissue_cluster_sizes = pd.read_csv(input_file, sep='\t', index_col=0)
vals = list(tissue_cluster_sizes.index)

tissue_cluster_sizes = tissue_cluster_sizes.set_index('META SOURCE')
tissue_cluster_fractions = tissue_cluster_sizes.div(tissue_cluster_sizes.sum(axis=1), axis=0)
# print(tissue_cluster_fractions)

# FORMAT BOXPLOT DATA
boxplot_data = []
pseudocount = 0.0001
for ii in np.arange(tissue_cluster_fractions.shape[0]):
    for jj in np.arange(tissue_cluster_fractions.shape[1]):
        boxplot_data.append({'META SOURCE': tissue_cluster_fractions.index[ii],
                             'CELL TYPE': tissue_cluster_fractions.columns[jj],
                             'FRACTION': np.log10(tissue_cluster_fractions.iloc[ii, jj] + pseudocount)})
boxplot_data = pd.DataFrame(boxplot_data)
# print(boxplot_data)

# GROUPED BOXPLOT WITH DATA POINTS OVERLAYED
fig = plt.figure(figsize=(pic_width, pic_height))
ax1 = plt.gca()
sns.set_style("white")

sns.boxplot(x="CELL TYPE", y="FRACTION", hue="META SOURCE", data=boxplot_data, palette=palette,
            hue_order=group_order, order=labels, fliersize=4, showmeans=False, linewidth=1)
g = sns.swarmplot(x="CELL TYPE", y="FRACTION", hue="META SOURCE", data=boxplot_data,
                  palette=dot_palette, edgecolor='#000000', linewidth=1, size=2,
                  hue_order=group_order, order=labels, dodge=True)
g.set_ylabel("\n\n\nLog10Fraction", fontsize=14, fontname='Arial')
g.set_xlabel("")
g.set_xticklabels(labels, rotation=90, fontname='Arial', fontsize=10)
g.tick_params(labelsize=14)
sns.despine()

ax1.legend_.remove()

# SAVE FIGURE
plt.savefig(figure_label + '.pdf', bbox_inches='tight', dpi=400)
plt.savefig(figure_label + '.png', bbox_inches='tight', dpi=400)


# 计算p值
outfile = figure_label + '.pvalue0.05.txt'
with open(outfile, 'w') as f:
    f.writelines('Cluster\tKruskalResult\n')
    for cell_query in list(tissue_cluster_fractions.columns):

        # SUBSET DATA FROM CELL TYPE
        tmp = tissue_cluster_fractions[cell_query]

        # 把所有分组存储到list中
        all_group = []
        for each_group in group_order:
            all_group.append(tmp[each_group])

        # list前加*可以把list解压开作为多个参数
        if stats.kruskal(*all_group)[1] < 0.05:
            # print(cell_query)
            # print(stats.kruskal(*all_group))
            f.writelines(cell_query)
            f.writelines('\t')
            f.writelines(str(stats.kruskal(*all_group)))
            f.writelines('\n')
