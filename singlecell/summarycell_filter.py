#! /usr/local/bin/python3
# coding:utf-8
"""
客户需要挑选很多cluster单独或合并后去做差异基因
提供需要的cluster，输出整理后的summarycell表格
"""
import os
import pandas as pd


def depart_cluster(need_cluster):
    cluster_raw = []
    cluster_chimera = []
    for each_cluster in need_cluster:
        if isinstance(each_cluster, int):
            cluster_raw.append(each_cluster)
        else:
            cluster_chimera.append(each_cluster)
    return cluster_raw, cluster_chimera


# 单个的Cluster合并在一个表格中输出，多个Cluster合并的在单独的表格中输出
# 针对的是需要在不同的cluster中进行样本间的比较
def filter_cluster1(infile, need_cluster):
    cluster_df = pd.read_csv(infile, sep='\t')
    cluster_raw, cluster_chimera = depart_cluster(need_cluster)
    print(cluster_raw, cluster_chimera)
    out_path = os.path.dirname(infile)
    # 根据单个cluster先进行一次过滤
    cluster_filter = cluster_df[cluster_df['Cluster'].isin(cluster_raw)]
    cluster_filter.to_csv(os.path.join(out_path, 'summarycell_filter.txt'), sep='\t', index=False)
    # 再根据合并的cluster进行过滤
    for each_cluster in cluster_chimera:
        clusters = each_cluster.split(';')
        clusters = list(map(int, clusters))
        cluster_df_tmp = cluster_df[cluster_df['Cluster'].isin(clusters)]
        cluster_label = list(set(cluster_df_tmp['Cluster']))
        cluster_label = list(map(str, cluster_label))
        cluster_label = '_'.join(cluster_label)
        cluster_df_tmp = pd.DataFrame({'Cell': cluster_df_tmp['Cell'],
                                       'Cluster': cluster_label})
        cluster_df_tmp.to_csv(os.path.join(out_path, f'Cluster{cluster_label}.txt'), sep='\t', index=False)


class MyCluster:
    def __init__(self, value):
        self.value = value

    def get_cluster(self):
        if isinstance(self.value, str):
            cluster_int = list(map(int, self.value.split(';')))
        else:
            cluster_int = [self.value]
        return cluster_int

    def get_label(self):
        if isinstance(self.value, str):
            cluster_label = '_'.join(self.value.split(';'))
        else:
            cluster_label = str(self.value)
        return cluster_label


# 要求的cluster不管是单个还是合并的，全在一个表格中输出
# 针对的是在单个样本中进行Cluster间的比较
# 要求need_cluster长度为2
def filter_cluster2(infile, need_cluster):
    cluster_df = pd.read_csv(infile, sep='\t')
    cluster1 = MyCluster(need_cluster[0])
    cluster2 = MyCluster(need_cluster[1])
    cluster1_value = set(cluster1.get_cluster())
    cluster2_value = set(cluster2.get_cluster())
    if not cluster1_value.intersection(cluster2_value):
        cluster_df_filter1 = cluster_df[cluster_df['Cluster'].isin(cluster1_value)]
        cluster_df_tmp1 = pd.DataFrame({'Cell': cluster_df_filter1['Cell'],
                                        'Cluster': cluster1.get_label()})
        cluster_df_filter2 = cluster_df[cluster_df['Cluster'].isin(cluster2_value)]
        cluster_df_tmp2 = pd.DataFrame({'Cell': cluster_df_filter2['Cell'],
                                        'Cluster': cluster2.get_label()})
        cluster_df_tmp = pd.concat([cluster_df_tmp1, cluster_df_tmp2], ignore_index=True)
        out_path = os.path.dirname(infile)
        cluster_df_tmp.to_csv(os.path.join(out_path, f'Cluster{cluster1.get_label()}and{cluster2.get_label()}.txt'),
                              sep='\t', index=False)
    else:
        print('输入的Cluster有重复，请检查')


if __name__ == "__main__":
    summarycell = r'C:\Users\asus\Desktop\1\test2\GraphClust.Summary_Cell.txt'
    # cluster中如果选择多个cluster，用英文分号分割
    # cluster = [0, 1, '2;3', '1;2;3']
    cluster = ['0;2;5', 14, '8;12;13', 6]
    # 注意选择filter_cluster1或filter_cluster2，功能不同
    filter_cluster1(summarycell, cluster)
