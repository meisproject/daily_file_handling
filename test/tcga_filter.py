#! /usr/local/bin/python3
# coding:utf-8
"""
根据TCGA clinicalMatrix.clinicalMatrix表格里的样本临床信息，筛选对应的样本fpkm
例如将样本按照MSS和MSI分别筛选出来
注意，临床数据表格中需要os_time在第5列，os在第6列，vital status在第91列
因为临床数据中的样本名不是都统一在一列中的，而是分布在多列中，所以需要根据fpkm中的样本进行查找
"""
import os
import pandas as pd


class TcgaSample:
    """
    TCGA每个样本信息（样本名，类型，os_time，os，生存状态）
    上面这个类型，指后续判断是否需要过滤的类型
    """
    __slots__ = ['sample', 'tcga_type', 'os_time', 'tcga_os', 'vital_status']

    def __init__(self, sample, tcga_type, os_time, tcga_os, vital_status):
        self.sample = sample
        self.tcga_type = tcga_type
        self.os_time = os_time
        self.tcga_os = tcga_os
        self.vital_status = vital_status


def get_sample_info(clinical, info_col, fpkm):
    """

    :param clinical: 临床数据总表
    :param info_col: 需要过滤的信息在临床数据里的第几列
    :param fpkm: TCGA中的fpkm表格
    :return: 每个样本对应的info信息（以fpkm表格的样本名为准）
    """

    all_sample_infos = []

    # 获取fpkm表格中所有样本名
    with open(fpkm) as f:
        line = f.readline()
        line = line.strip('\n')
        fpkm_sample = line.split('\t')
        fpkm_sample.pop(0)
        # print(fpkm_sample)

    # 在临床数据中查找fpkm样本对应的信息
    with open(clinical) as f2:
        for each_sample in fpkm_sample:
            # print(each_sample)
            sample_type = []
            os_time = []
            tcga_os = []
            vital_status = []
            # print(each_sample)
            # 这里一定要重新定位到文件开头，不然下面的循环不能运行……
            f2.seek(0)
            for linenum, line in enumerate(f2, 1):
                # print(line)
                if each_sample in line:
                    type_name = line.split('\t')[info_col - 1]
                    sample_type.append(type_name)
                    os_time.append(line.split('\t')[4])
                    tcga_os.append(line.split('\t')[5])
                    vital_status.append(line.split('\t')[90])
            if len(sample_type) > 1:
                print(f'{each_sample} has {len(sample_type)} types, please check!')
            elif not sample_type:
                print(f'{each_sample} has no type, please check!')
            tmp_sample = TcgaSample(each_sample, sample_type, os_time, tcga_os, vital_status)
            all_sample_infos.append(tmp_sample)
    return all_sample_infos


def filter_info(all_sample_infos, info, clinical_result):
    """
    将过滤后的样本名和对应的info输出到txt中，并返回过滤后的样本名

    :param all_sample_infos: 由get_sample_info返回的值
    :param info: 需要保留的信息
    :param clinical_result:过滤后的临床数据文件名
    :return:过滤后的样本名
    """
    new_sample_types = []
    with open(clinical_result, 'w') as f:
        f.write('SampleID\tbcr_patient_barcode\tOS.time\tOS\tVital Status\n')
        for each_sample in all_sample_infos:
            actual_info = ','.join(each_sample.tcga_type)
            if info in actual_info:
                new_sample_types.append(each_sample.sample)
                tmp_os_time = ','.join(each_sample.os_time)
                tmp_os = ','.join(each_sample.tcga_os)
                tmp_status = ','.join(each_sample.vital_status)
                f.write(f'{each_sample.sample}\t{each_sample.sample}\t{tmp_os_time}\t{tmp_os}\t{tmp_status}\n')
    # print(new_sample_types)
    return new_sample_types


def tcga_filter(clinical, info_col, info, fpkm):
    """
    输出过滤后的tcga fpkm数据
    :param clinical:临床数据总表
    :param info_col:需要过滤的信息在临床数据里的第几列
    :param info:需要保留的信息
    :param fpkm:TCGA中的fpkm表格
    """
    sample_types = get_sample_info(clinical, info_col, fpkm)
    clinical_df_name = os.path.join(os.path.dirname(fpkm), 'clinical_filtered.txt')
    filtered_sample = filter_info(sample_types, info, clinical_df_name)
    fpkm_df = pd.read_csv(fpkm, sep='\t')
    first_col = fpkm_df.columns[0]
    filtered_sample.insert(0, first_col)
    fpkm_filter = fpkm_df.loc[:, filtered_sample]
    result_name = os.path.join(os.path.dirname(fpkm), 'TCGA_filtered.txt')
    fpkm_filter.to_csv(result_name, sep='\t', index=False)


if __name__ == "__main__":
    clinical_dat = r'C:\Users\asus\Desktop\1\test2\TCGA-THCA_clinicalMatrix'
    clinical_col = 2
    clinical_info = 'MSI'
    fpkm_dat = r'C:\Users\asus\Desktop\1\test2\TCGA-STAD.FPKM.tsv'
    tcga_filter(clinical_dat, clinical_col, clinical_info, fpkm_dat)
