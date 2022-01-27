#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
# 提取离lncRNA最近的mRNA（李琳售后用）
import os


def get_lnc_mrna(path, lnc, mrna):
    with open(os.path.join(path, lnc)) as lnc_f:
        for i, line in enumerate(lnc_f):
            if i == 0:
                with open(os.path.join(path, 'nearest_mRNA.txt'), 'w') as result:
                    result.writelines(line.rstrip('\n') + '\tmRNA_GeneID\tmRNA_transcriptID\tmRNA_CHROM\tmRNA_Start'
                                                          '\tmRNA_End\tmRNA_strand\tmRNA_distance2lncRNA\tmRNA_symbol'
                                                          '\tmRNA_description\n')
                continue
            chrom = line.rstrip('\n').split('\t')[2]
            start = line.rstrip('\n').split('\t')[3]
            end = line.rstrip('\n').split('\t')[4]
            overlap_list = []
            other_list = []
            distance_list = []
            with open(os.path.join(path, mrna)) as mrna_f:
                for n_line in mrna_f:
                    n_chrom = n_line.rstrip('\n').split('\t')[0]
                    n_start = n_line.rstrip('\n').split('\t')[3]
                    n_end = n_line.rstrip('\n').split('\t')[4]
                    n_strand = n_line.rstrip('\n').split('\t')[5]
                    n_id = n_line.rstrip('\n').split('\t')[7]
                    n_parent = n_line.rstrip('\n').split('\t')[8]
                    n_symbol = n_line.rstrip('\n').split('\t')[9]
                    n_des = n_line.rstrip('\n').split('\t')[11]
                    if n_chrom == chrom:
                        if int(start) <= int(n_start) <= int(end) or int(start) <= int(n_end) <= int(end):  # 判断重叠
                            overlap_list.append([n_parent, n_id, n_chrom, n_start, n_end, n_strand, 0, n_symbol, n_des])
                        elif int(n_start) < int(start) and int(n_end) > int(end):  # 判断重叠
                            overlap_list.append([n_parent, n_id, n_chrom, n_start, n_end, n_strand, 0, n_symbol, n_des])
                        elif int(n_start) > int(end):  # 非重叠
                            distance = int(n_start) - int(end)
                            other_list.append([n_parent, n_id, n_chrom, n_start, n_end, n_strand, distance,
                                               n_symbol, n_des])
                            distance_list.append(distance)
                        elif int(n_end) < int(start):  # 非重叠
                            distance = int(start) - int(n_end)
                            other_list.append([n_parent, n_id, n_chrom, n_start, n_end, n_strand, distance,
                                               n_symbol, n_des])
                            distance_list.append(distance)
            with open(os.path.join(path, 'nearest_mRNA.txt'), 'a') as result:
                if len(overlap_list) > 0:  # 如果有overlap基因
                    for overlap in overlap_list:
                        result.writelines(line.rstrip('\n'))
                        for eve_over in overlap:
                            result.writelines('\t' + str(eve_over))
                        result.writelines('\n')
                else:
                    result.writelines(line.rstrip('\n'))
                    max_dis = distance_list.index(min(distance_list))  # 找出最小距离
                    # print(chrom + ':' + start + '-' + end + '长度' + str(max_dis))
                    for info in other_list[max_dis]:
                        result.writelines('\t' + str(info))
                    result.writelines('\n')


if __name__ == "__main__":
    inpath = r'C:\Users\asus\Desktop\1'
    lncrna = r'down.txt'
    mrna_file = r'所有mRNA位置.txt'
    get_lnc_mrna(inpath, lncrna, mrna_file)