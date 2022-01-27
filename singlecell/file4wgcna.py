#! /usr/local/bin/python3
# coding:utf-8
"""
根据trait表格和各个细胞细分的cellumiinfo整理WGCNA需要的上传表格
"""
import os
import pandas as pd


def treat_file(each_cellumiinfo, trait):
    umiinfo = pd.read_csv(each_cellumiinfo, sep='\t')
    trait_df = pd.read_csv(trait, sep='\t')
    # 生成最后输出的文件名
    group_name = os.path.basename(each_cellumiinfo)
    umiinfo_name = os.path.join(os.path.dirname(trait), group_name)
    trait_name = umiinfo_name.replace('.txt', '_trait.txt')
    # CellUmiinfo只留细胞名和样本名列
    umiinfo = umiinfo.loc[:, ['CellName', 'orig.ident']]
    umiinfo.to_csv(umiinfo_name, sep='\t', index=False)
    # 根据cellumiinfo筛选trait信息
    raw_columns = list(trait_df.columns)
    raw_columns[0] = 'Sample'
    trait_df.columns = raw_columns
    all_samples_raw = list(umiinfo.iloc[:, 1])
    all_samples = list(set(all_samples_raw))
    all_samples.sort(key=all_samples_raw.index)   # 按照原本的样本顺序对去重后的样本进行排序
    # 筛选样本，并按照cellumiinfo中的样本顺序对trait表格排序
    trait_filter = trait_df[trait_df['Sample'].isin(all_samples)]
    trait_filter.index = list(trait_filter['Sample'])
    trait_filter = trait_filter.reindex(all_samples)
    # print(trait_filter)
    # 剔除没有样本的分组
    trait_filter = trait_filter.loc[:, (trait_filter != 0).any(axis=0)]
    trait_filter.to_csv(trait_name, sep='\t', index=False)
    # print(trait_filter)


def treat_files(cellumiinfo, trait):
    all_cellumiinfo = os.listdir(cellumiinfo)
    for each_cellumiinfo in all_cellumiinfo:
        treat_file(os.path.join(cellumiinfo, each_cellumiinfo), trait)


if __name__ == "__main__":
    cellumiinfo_path = r'C:\Users\asus\Desktop\1\test2\cellumiinfo'
    trait_file = r'C:\Users\asus\Desktop\1\test2\Trait.txt'
    treat_files(cellumiinfo_path, trait_file)
