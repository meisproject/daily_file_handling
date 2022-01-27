#! /usr/local/bin/python3
# coding:utf-8
# 根据ACFS2预测得到的circRNA序列和circBase数据库下载的序列，对ACFS2预测的circRNA进行circBase ID注释
# 因为预测采用的是人GRCh38和小鼠mm10的基因组版本，而circBase采用的是人GRCh37和小鼠mm9的基因组版本，所以无法直接根据基因组位置进行判断
# 采用序列进行判断，判断标准：1.序列完全一致 2.host基因一致
# 可能存在的问题：circBase数据库中有部分circRNA的序列完全一致，host基因也完全一致，需要额外进行判断
from multiprocessing import Pool
import multiprocessing
import time
import os
import re
from fasta_cut_into_piece import seq_cut
import mul_process_package


# 统一fa格式
def fa_trans(file):
    seq = {}
    for line in file:
        if line.startswith('>'):
            global name
            name = line.replace('>', '')
            seq[name] = ''
        else:
            if line in ['\n', '\r\n']:  # 判断是否空行
                seq.pop(name)  # pop：dict删除key
                continue
            seq[name] += line.replace('\n', '')
    return seq


# 合并拆分后分别获得的文件
def catfile2(fdir):
    filenames = os.listdir(fdir)
    f = open(os.path.join(fdir, 'FinalResult.txt'), 'w')
    for filename in filenames:
        if filename.endswith('result.txt'):
            filepath = os.path.join(fdir, filename)
            for line in open(filepath):
                f.writelines(line)
    f.close()


# 判断序列是否一致，如果出现一对多则进行提示
def fa_estimate(source, target, rfile, flag):
    sourceseq = fa_trans(source)
    with open(target, 'r') as targetfile:
        targetseq = fa_trans(targetfile)
    with open(os.path.join(rfile, str(flag) + r'result.txt'), 'w') as result:
        for si in sourceseq.keys():
            count = 0
            for j in targetseq.keys():
                if sourceseq[si] == targetseq[j]:
                    result.write(si.split('\n')[0] + '\t' + j)
                    count += 1
                    # break (加上break的话只匹配第一个一致的，速度会快，但是无法发现一对多现象）
            if count > 1:
                print(si + u'对应多个序列，请注意审查')


# 判断host基因是否一致
def hostgene_estimate(file, outfile):
    with open(outfile, "w") as f1:
        f1.writelines('AccID' + '\t' + 'CircBaseID' + '\t' + 'circBaseSeq_ID' '\n')
        with open(file) as f:
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.rstrip('\n')
                predict_name = line.split('\t')[0]
                circbase_name = line.split('\t')[1]
                # 提取预测和circBase ID中的host基因
                predict_host = re.findall(r'chr.+_\d+_\d+_[+-]\d+-(.+)', predict_name)
                circbase_host = re.findall(r'.+[|]chr.+[|].+[|](.+)', circbase_name)
                # 因为ACSF2预测的circRNA名字中如果没有host基因，host基因会写成na
                # 而circBase数据库如果没有host基因，会写成None，两边统一后进行比较
                if circbase_host[0] == 'None':
                    circbase_host[0] = 'na'
                circbase_id = re.findall(r'(.+)[|]chr.+[|].+[|].+', circbase_name)
                if predict_host == circbase_host:
                    f1.writelines(predict_name + '\t' + circbase_name + '\t' + circbase_id[0] + '\n')


if __name__ == '__main__':
    multiprocessing.freeze_support()
    # s = input(r'请输入要注释的circRNA序列文件路径（格式如C:\Users\asus\Desktop\1\circRNA.fa）：')  # 平台预测circRNA
    # t = input(r'请输入circBase序列路径（格式同上）：')  # circBase
    # rf = input(r'请输入输出文件路径（格式如C:\Users\asus\Desktop\1）：')    # 输出文件路径
    s = r'C:\Users\asus\Desktop\1\all.circRNA.fa'  # 平台预测circRNA
    t = r'F:\1.梅姗姗_第二批\个人\2.代码\4.python\test\circBaseID注释\mouse_mm9_circRNAs_putative_spliced_sequence.fa'  # circBase
    rf = r'C:\Users\asus\Desktop\1'    # 输出文件路径
    start = time.time()
    file_list = seq_cut(s)  # 如果序列超过平台预测circRNA超过10000个，切分为4个
    if len(file_list) > 1:  # 如果做了切分，4个进程并行
        print(u'序列太多啦，切成4份同时运行，请等待……')
        p = Pool(4)
        for i in range(4):
            p.apply_async(fa_estimate, args=(file_list[i], t, rf, i))
        p.close()  # 关闭进程池，不再添加新进程
        p.join()  # 等待进程池中进程完成
        catfile2(rf)  # 合并生成的文件
        for i in range(4):
            os.remove(os.path.join(rf, str(i) + r'result.txt'))  # 删除生成的分文件
        # 判断host基因是否一致，只保留host基因一致的circRNA
        hostgene_estimate(os.path.join(rf, 'FinalResult.txt'), os.path.join(rf, 'FinalResult_filtered.txt'))
        os.remove(os.path.join(rf, 'FinalResult.txt'))
    else:
        print(u'序列数量还行，直接运行，请等待……')
        sfile = open(s, 'r')
        i = ''
        fa_estimate(sfile, t, rf, i)
        sfile.close()
        # 判断host基因是否一致，只保留host基因一致的circRNA
        hostgene_estimate(os.path.join(rf, 'result.txt'), os.path.join(rf, 'FinalResult_filtered.txt'))
        os.remove(os.path.join(rf, 'result.txt'))
    end = time.time()
    print(u'circBase ID注释完成，耗时 %0.2f 秒' % (end - start))
    # input('Press Enter to exit...')

