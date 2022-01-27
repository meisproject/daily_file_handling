#! /usr/local/bin/python3
# coding:utf-8
# 提取miranda或RNAhybrid的靶基因结合情况
import linecache  # 专门支持读取大文件，而且支持行式读取的函数库
import os
import re


# 获取挑选的miRNA、靶基因、结合起始位点和终止位点信息
def get_info(path, file, t_type):
    select_loc = []
    with open(os.path.join(path, file)) as f:
        for i, line in enumerate(f):
            info = line.split('\t')
            if i == 0:
                for j, name in enumerate(line.split('\t')):
                    if name == 'StartSubject' or ('StartSubject_' + t_type) in name:
                        global start_sub
                        start_sub = j
                continue
            else:
                give_info = [info[0], info[1], info[start_sub], info[start_sub+1].split('\n')[0]]
                select_loc.append(give_info)
    # print(select_loc)
    return select_loc


# 将RNAhybrid拆成两行写的序列合并
def mix_sequence(aa, bb):
    cc = []
    aa = aa.replace(' ', '-')
    bb = bb.replace(' ', '-')
    for i in range(0, len(aa)):
        if aa[i] == '-':
            cc.append(bb[i])
        else:
            cc.append(aa[i])
    return cc


# 判断RNAhybrid结合键
def bond_estimate(aa, bb):
    cc = []
    for i in range(0, len(aa)-1):
        if aa[i] == '-' or bb[i] == '-':
            cc.append(' ')
        else:
            if str.upper(aa[i]) == 'A':
                if str.upper(bb[i]) == 'U':
                    cc.append('|')
                else:
                    cc.append(':')
            if str.upper(aa[i]) == 'U':
                if str.upper(bb[i]) == 'A':
                    cc.append('|')
                else:
                    cc.append(':')
            if str.upper(aa[i]) == 'C':
                if str.upper(bb[i]) == 'G':
                    cc.append('|')
                else:
                    cc.append(':')
            if str.upper(aa[i]) == 'G':
                if str.upper(bb[i]) == 'C':
                    cc.append('|')
                else:
                    cc.append(':')
    cc.append(' ')
    cc = ''.join(cc)
    return cc


# 根据ref序列和bond信息判断结合类型
def type_estimate(target_seq, bond_seq):
    if bond_seq[-7:-1] == r'||||||':
        if bond_seq[-8] == r'|':
            if str.upper(target_seq[-1]) == 'A':
                bond_type = '8mer'
            else:
                bond_type = '7mer-m8'
        else:
            if str.upper(target_seq[-1]) == 'A':
                bond_type = '7mer-A1'
            else:
                bond_type = 'no'
                # print('6mer')
    else:
        bond_type = 'no'
        # print('Offset 6mer')
    return bond_type


# miranda靶基因结合关系提取（miranda关系有重复，根据位置信息再判断）
def miranda_extract(path, allre, select_info):
    head = r'Performing Scan: ' + select_info[0] + ' vs ' + select_info[1]
    tail = r'>>' + select_info[0] + '\t' + select_info[1]
    # 找到关系所在行
    with open(os.path.join(path, allre)) as f:
        for i, line in enumerate(f):  # enumerate可以使list变成索引-元素对
            if line.startswith(head):
                global start
                start = i
            elif line.startswith(tail):
                global end
                end = i
                break

    # 提取关系所在的整行内容
    tfile = os.path.join(path, select_info[0] + 'vs' + select_info[1] + r'_temp.txt')
    with open(tfile, 'w') as tempfile:
        for l in range(start + 1, end + 2):
            count = linecache.getline(os.path.join(path, allre), l)
            tempfile.writelines(count)

    with open(tfile, 'r') as tempfile:
        # Type = "no"
        loc = []
        for j, line in enumerate(tempfile):
            if line.startswith('   Forward:'):
                loc.append(j)
        # print(loc)
    # 获取具体信息
    per_scan = select_info[0] + ' vs ' + select_info[1]  # 标题信息
    re_s1 = re.compile('\s+Forward.+R:')
    re_s2 = re.compile('\sto.+\n')
    re_e1 = re.compile('\s+Forward.+R:.+to\s')
    re_e2 = re.compile('\sAlign.+\n')
    all_info = []
    for k in loc:
        q = linecache.getline(tfile, k + 3)[16:-4]  # Query信息（select_info[0]）
        bond = linecache.getline(tfile, k + 4)[16:-1]  # 结合信息
        r = linecache.getline(tfile, k + 5)[16:-4]  # Ref信息（mRNA/ncRNA/circRNA）
        s_and_e = linecache.getline(tfile, k + 1)
        s = re.sub(re_s1, '', s_and_e)
        s = re.sub(re_s2, '', s)  # 结合起始位置
        e = re.sub(re_e1, '', s_and_e)
        e = re.sub(re_e2, '', e)  # 结合终止位置
        t = type_estimate(r, bond)
        info = [per_scan, q, bond, r, s, e, t]
        if s == select_info[2] and e == select_info[3]:  # 只保留和挑选靶基因预测结合位置一致的条目
            all_info.append(info)
        # print(per_scan + '\n' + q + '\n' + bond + '\n' + r + '\n' + 'start:' + s + ' end:' + e + '\n' + t)
    os.remove(tfile)
    # print(all_info)
    return all_info


# RNAhybrid靶基因结合关系提取（RNAhybrid无重复关系?)
def rnahybrid_extract(path, allre, select_info):
    head = 'target: ' + select_info[1]
    # 找到关系所在行
    with open(os.path.join(path, allre)) as f:
        for i, line in enumerate(f):  # enumerate可以使list变成索引-元素对
            tail = linecache.getline(os.path.join(path, allre), i + 3)
            if line.startswith(head) and tail == 'miRNA : ' + select_info[0] + '\n':
                global st
                st = i
                break

    # 提取关系所在的整行内容
    tfile = os.path.join(path, select_info[0] + 'vs' + select_info[1] + r'_temp.txt')
    with open(tfile, 'w') as tempfile:
        for l in range(st + 1, st + 14):
            count = linecache.getline(os.path.join(path, allre), l)
            tempfile.writelines(count)

    per_scan = select_info[0] + ' vs ' + select_info[1]  # 标题信息
    t_1 = linecache.getline(tfile, 10)
    t_2 = linecache.getline(tfile, 11)
    m_1 = linecache.getline(tfile, 12)
    m_2 = linecache.getline(tfile, 13)
    t_all = ''.join(mix_sequence(t_1, t_2))[10:-4]  # target基因序列信息
    m_all = ''.join(mix_sequence(m_1, m_2))[10:-4]  # miRNA序列信息
    bond = bond_estimate(t_all, m_all)
    target_start = linecache.getline(tfile, 9)[10:-1]  # 靶基因结合起始位点
    pure_t = re.sub('^-+', '', t_all)
    target_end = int(target_start) + len(pure_t) - 1  # 靶基因结合终止位点
    pure_bond = re.sub('^-+', '', bond)
    t = type_estimate(pure_t, pure_bond)
    info = [per_scan, m_all, bond, t_all, target_start, str(target_end), t]
    # print(per_scan + '\n' + t_all + '\n' + bond + '\n' + m_all + '\n' + 'start:' + target_start +
    # ' end:' + str(target_end) + '\n' + t)
    os.remove(tfile)
    return info


if __name__ == "__main__":
    filepath = input(r'请输入文件夹路径（如：C:\Users\asus\Desktop\1）：')
    targetfile = input(r'请输入解压后的靶基因结合文件名（如：miRNAVScircRNA.targetPredict.RNAhybrid）：')
    selected = input(r'请输入挑选的靶基因关系文件名（如：selected.txt）（格式同平台直接下载的文件）：')
    if targetfile.endswith('miranda'):
        target_type = 'Miranda'
        print(u'靶基因预测软件为%s，运行结束后会自动关闭，请等待……' % targetfile)
        sele_rela = get_info(filepath, selected, target_type)
        with open(os.path.join(filepath, 'FinalResult.txt'), 'w') as result:
            result.writelines('PerformingScan\tQuery\tbond\tRef\tStart\tEnd\tType\n')
        for value in sele_rela:
            a_info = miranda_extract(filepath, targetfile, value)
            with open(os.path.join(filepath, 'FinalResult.txt'), 'a') as result:
                for inf in a_info:
                    result.write('\t'.join(inf) + '\n')

    if targetfile.endswith('RNAhybrid'):
        target_type = 'RNAhybrid'
        print(u'靶基因预测软件为%s，运行结束后会自动关闭，请等待……' % targetfile)
        sele_rela = get_info(filepath, selected, target_type)
        with open(os.path.join(filepath, 'FinalResult.txt'), 'w') as result:
            result.writelines('PerformingScan\tQuery\tbond\tRef\tStart\tEnd\tType\n')
        for value in sele_rela:
            a_info = rnahybrid_extract(filepath, targetfile, value)
            with open(os.path.join(filepath, 'FinalResult.txt'), 'a') as result:
                result.write('\t'.join(a_info) + '\n')

