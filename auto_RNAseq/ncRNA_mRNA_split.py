#! /usr/local/bin/python3
# coding:utf-8
"""
将xlsx格式的差异基因按照lncRNA和mRNA分开成两个表格

pandas输出xlsx的title格式修改参考https://xlsxwriter.readthedocs.io/example_pandas_header_format.html
"""
import os
import pandas as pd


def new_to_excel(context, filename):
    """
    将pandas默认输出excel的title格式全都去除

    :param context: pandas中存储的表格信息
    :param filename: 输出的文件名
    """
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    context.to_excel(writer, sheet_name='Sheet1', index=False, startrow=1, header=False)
    worksheet = writer.sheets['Sheet1']
    for col_num, value in enumerate(context.columns.values):
        worksheet.write(0, col_num, value)
    writer.save()


def celltype_split(file):
    """

    :param file: 需要提取mRNA和ncRNA的文件
    """
    p = pd.read_excel(file)
    # ncRNA筛选
    p_ncrna = p[p['GeneType'].isin(["IG_C_pseudogene", "IG_J_pseudogene", "IG_pseudogene", "IG_V_pseudogene", "lncRNA",
                                    "polymorphic_pseudogene", "processed_pseudogene", "pseudogene", "rRNA_pseudogene",
                                    "TR_J_pseudogene", "TR_V_pseudogene", "transcribed_processed_pseudogene",
                                    "transcribed_unitary_pseudogene", "transcribed_unprocessed_pseudogene",
                                    "translated_processed_pseudogene", "translated_unprocessed_pseudogene",
                                    "unitary_pseudogene", "unprocessed_pseudogene"])]
    # new_to_excel(p_ncrna, file.replace('.xlsx', '_ncRNA.xlsx'))
    p_lncrna = p_ncrna[p_ncrna['Transcript length (including UTRs and CDS)'] >= 200]
    new_to_excel(p_lncrna, file.replace('.xlsx', '_lncRNA.xlsx'))

    # mRNA筛选
    p_mrna = p[p['GeneType'].isin(['protein-coding', 'protein_coding'])]
    new_to_excel(p_mrna, file.replace('.xlsx', '_mRNA.xlsx'))


if __name__ == "__main__":
    path = r'C:\Users\asus\Desktop\1\test2'
    all_files = os.listdir(path)
    for each_file in all_files:
        if each_file.endswith('.xlsx'):
            celltype_split(os.path.join(path, each_file))
