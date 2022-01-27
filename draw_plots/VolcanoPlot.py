#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
# 正常火山图、标注基因火山图和按照Term标注（如果FDR、Pvalue为0，该基因无法显示）
import os
import glob
# import math
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import numpy as np  # Scientific computing
import pandas as pd  # Data analysis
from adjustText import adjust_text  # 自动调整文字间距


def volcano(path, file, para):
    data = pd.read_csv(os.path.join(path, file), sep='\t')  # 读取表格
    data = data.fillna('')  # 将NaN替换为空值
    fdr = data.iloc[:, int(para[0]-1)]  # 按列数取值
    fc = data.iloc[:, int(para[1]-1)]
    fdr_normolize = -np.log10(fdr)  # -log10(FDR)
    result = pd.concat([fdr, fdr_normolize, fc], axis=1, ignore_index=True)  # 合并series为dataframe
    result.columns = ['FDR', 'FDR_Norm', 'FC']
    # dataframe的loc可以按照逻辑值或者str对行列进行筛选
    result_up = result.loc[(result['FC'] > para[3]) & (result['FDR'] < para[2]), ]  # 上调基因
    result_down = result.loc[(result['FC'] < -para[3]) & (result['FDR'] < para[2]), ]  # 下调基因
    result_normal = result.loc[(abs(result['FC']) < para[3]) | (result['FDR'] > para[2]), ]  # 不差异基因
    # x_pos = math.ceil(np.percentile(result_up['FC'], 90))  # np.percentile取分位数
    # x_neg = math.floor(np.percentile(result_down['FC'], 10))  # math.ceil向上取整
    # y_max = np.percentile(result['FDR_Norm'], 99.5)  # math.floor向下取整
    # 开始画图
    prop = fm.FontProperties(fname=r'C:\Windows\Fonts\arial.ttf')
    fig = plt.figure(figsize=(7, 8))
    ax = fig.add_subplot(111)
    plt.ylim(-5, 50)
    '''
    # 如果基因数多余50个，调整X、Y轴范围（如果y最大的点对应的x比x_pos1.1或x_neg*1.1绝对值大，上方会有大片空白）（需要改）
    if len(result) > 50:
        plt.xlim(x_neg * 1.1, x_pos * 1.1)
        if not y_max == float("inf") or y_max == -float("inf"):
            print(max(result['FDR_Norm']))
            if y_max * 1.5 > max(result['FDR_Norm']):
                plt.ylim(0 - 0.02 * y_max, max(result['FDR_Norm']))
            else:
                y_max = math.ceil(y_max)
                plt.ylim(0 - 0.02 * y_max, math.ceil(y_max * 1.5))
    '''
    # 画点，如果没有挑选的条目，直接按照上下调加颜色，否则按照条目加颜色
    if not para[5]:
        if len(result_normal) > 0:
            ax.scatter(x=result_normal['FC'], y=result_normal['FDR_Norm'], c='grey', label='normal', s=6)
        if len(result_up) > 0:
            ax.scatter(x=result_up['FC'], y=result_up['FDR_Norm'], c='r', label='up', s=6)
        if len(result_down) > 0:
            ax.scatter(x=result_down['FC'], y=result_down['FDR_Norm'], c='b', label='down', s=6)
        # 加上卡值范围线
        plt.axvline(para[3], linestyle="dotted", linewidth=1, color='k')
        plt.axvline(-para[3], linestyle="dotted", linewidth=1, color='k')
        plt.axhline(-np.log10(para[2]), linestyle="dotted", linewidth=1, color='k')
    else:
        term = data.iloc[:, int(para[5]-1)]
        term = term.mask(term == '', 'other')  # mask：条件为真时，替换
        result_term = pd.concat([fdr, fdr_normolize, fc, term], axis=1, ignore_index=True)  # 合并series为dataframe
        result_term.columns = ['FDR', 'FDR_Norm', 'FC', 'Term']
        all_num = list(range(0, len(term.drop_duplicates())))
        term_redu = term.drop_duplicates().to_list()
        for num in all_num:
            term_sle = result_term.loc[result_term['Term'] == term_redu[num], ]
            if term_redu[num] == 'other':
                ax.scatter(x=term_sle['FC'], y=term_sle['FDR_Norm'], c='grey', label=term_redu[num], s=6)
                continue
            ax.scatter(x=term_sle['FC'], y=term_sle['FDR_Norm'], label=term_redu[num], s=6)
    # 加上标题和legend
    plt.legend(handlelength=0.3)
    ax.set_xlabel(r'$log_2(FC)$', fontweight='bold', fontproperties=prop, fontsize=20)
    if 'FDR' in str.upper(fdr.name):
        ax.set_ylabel(r'$-log_{10}(FDR)$', fontweight='bold', fontproperties=prop, fontsize=20)
    else:
        ax.set_ylabel(r'$-log_{10}(P-value)$', fontweight='bold', fontproperties=prop, fontsize=20)
    plt.title('VolcanoPlot', loc='left', fontproperties=prop, fontsize=30)
    # 加上需要标注的基因
    if para[4]:
        data_sele = data.loc[data.iloc[:, int(para[4]-1)] != '', ]
        fdr_sele = data_sele.iloc[:, int(para[0] - 1)]
        fc_sele = data_sele.iloc[:, int(para[1] - 1)]
        gene_sele = data_sele.iloc[:, int(para[4] - 1)]
        fdr_sele_normolize = -np.log10(fdr_sele)
        result_sele = pd.concat([fdr_sele, fdr_sele_normolize, fc_sele, gene_sele], axis=1, ignore_index=True)
        result_sele.columns = ['FDR', 'FDR_Norm', 'FC', 'gene']
        ax.scatter(x=result_sele['FC'], y=result_sele['FDR_Norm'], c='', linewidths=1.5, s=50, edgecolors='k')
        # zip() 函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的对象
        text_loc = zip(result_sele['FC'], result_sele['FDR_Norm'], result_sele['gene'])
        texts = [plt.text(x=fc_s * 1, y=fdr_ns, s=gene_s, fontweight='semibold', fontproperties=prop, fontsize=20,
                          bbox=dict(facecolor='w', alpha=0.4, edgecolor='w', pad=0.15))
                 for fc_s, fdr_ns, gene_s in text_loc]
        adjust_text(texts, arrowprops=dict(arrowstyle='->', color='black'))
    matplotlib.rcParams['svg.fonttype'] = 'none'  # 更改matplolib配置，输出文字为文本对象，而不是默认的路径
    plt.savefig(os.path.join(path, os.path.splitext(file)[0] + '.svg'))
    plt.savefig(os.path.join(path, os.path.splitext(file)[0] + '.png'), dpi=400)
    plt.savefig(os.path.join(path, os.path.splitext(file)[0] + '.pdf'))
    # plt.show()
    # with pd.ExcelWriter(os.path.join(path, r'forVolcano.xlsx')) as writer:
    # result.to_excel(writer,index=False)


if __name__ == "__main__":
    filedir = r'C:\Users\asus\Desktop\1'
    filename = r'DN-OsxVsWT.txt'
    filelist = glob.glob(os.path.join(filedir, r'*.txt*'))
    fdr_pvalue = 4
    log2fc = 2
    fdr_cutoff = 0.05
    fc_cutoff = 1
    selected_gene = 11
    selected_Term = ''
    parameter = [fdr_pvalue, log2fc, fdr_cutoff, fc_cutoff, selected_gene, selected_Term]
    volcano(filedir, filename, parameter)
    # for filename in filelist:
        # volcano(filedir, filename, parameter)
