#! /usr/local/bin/python3
# coding:utf-8
# 用总的基因做好GeneActNet后，在所有关系中挑选出树状的差异基因相关的关系条目
# 有一个问题，不知道为啥每次运行出来的结果顺序都不一样
# 最终输出的表格是有重复项的，需要自己另外删除重复项
import pandas as pd


def relation_select(dif_file, all_file, output):
    # difgene为差异基因list
    difgene = pd.read_csv(dif_file, sep='\t')
    difgene = set(difgene['AccID'])

    # relation_raw是source和target的对应dict
    # relation里同时存放了source:target和target:source
    relation = dict()
    relation_raw = dict()
    flag = 1
    with open(all_file) as f1:
        while True:
            line = f1.readline()
            if not line:
                break
            if flag != 1:
                line = line.strip('\n')
                source = line.split('\t')[0]
                target = line.split('\t')[1]
                if relation_raw.get(source) is not None:
                    relation_raw[source].append(target)
                else:
                    relation_raw[source] = list()
                    relation_raw[source].append(target)
                # relation里把source:target和target:source都记录一遍
                if relation.get(source) is not None:
                    relation[source].append(target)
                else:
                    relation[source] = list()
                    relation[source].append(target)
                if relation.get(target) is not None:
                    if source not in relation.get(target):
                        relation[target].append(source)
                else:
                    relation[target] = list()
                    relation[target].append(source)
            flag = flag + 1
    print(relation)

    # 获取source基因中的差异基因
    sourcedif = difgene & set(relation.keys())
    # difrelation是从relation中抽取差异source对应的关系对
    difrelation = {sourcedifgene: relation.get(sourcedifgene) for sourcedifgene in sourcedif}
    # print(difrelation)

    # final_relation是最终挑选符合要求的关系
    final_relation = list()
    for key in difrelation.keys():
        # all_target是差异source对应的target基因
        all_target = difrelation.get(key)
        needremove = list()
        # 1.找到source和target都差异的关系，如果用.表示差异基因，?表示非差异基因，即._.
        # 并将找到的差异target从all_target里删除
        for eve_target in all_target:
            if eve_target in difgene:
                final_relation.append([key, eve_target])
                needremove.append(eve_target)
            else:
                continue
        for j in needremove:
            all_target.remove(j)
        # print(all_target)
        # 2.找到target不差异，但是target作为新的source时，新的target差异的关系，即._?_.
        if len(all_target) > 0:
            for eve_target2 in all_target:
                # all_target2是将原本的target作为source找到的target
                all_target2 = relation.get(eve_target2)
                if all_target2 is not None:
                    for eve_target3 in all_target2:
                        if (eve_target3 in difgene) & (eve_target3 != key):
                            final_relation.append([key, eve_target2])
                            final_relation.append([eve_target2, eve_target3])
                        # else:
                        #     # 3.再进一步套娃，即判断._?_?_.
                        #     all_target3 = relation.get(eve_target3)
                        #     if all_target3 is not None:
                        #         for eve_target4 in all_target3:
                        #             if (eve_target4 in difgene) & (eve_target4 != key):
                        #                 final_relation.append([key, eve_target2])
                        #                 final_relation.append([eve_target2, eve_target3])
                        #                 final_relation.append([eve_target3, eve_target4])
    print(final_relation[0:5])

    # 判断final_relation是否在relation_raw里
    with open(output, 'w') as f2:
        f2.writelines('source' + '\t' + 'target' + '\n')
        for rela in final_relation:
            if relation_raw.get(rela[0]) is not None:
                if rela[1] in relation_raw.get(rela[0]):
                    f2.writelines(rela[0] + '\t' + rela[1] + '\n')


if __name__ == "__main__":
    # file1是差异基因表格，第一列是基因
    file1 = r'C:\Users\asus\Desktop\1\删样本.txt'
    # file2是总的GeneActNet
    file2 = r'C:\Users\asus\Desktop\1\GeneActRelation.Gene_Act_Net.gene.txt'
    outfile = r'C:\Users\asus\Desktop\1\最终选择.txt'
    relation_select(file1, file2, outfile)
