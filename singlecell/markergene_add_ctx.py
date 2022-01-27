#! /usr/local/bin/python3
# coding:utf-8
"""
在GraphClust.AllMarkerGenes.txt表格中加上ctx整理得到的对应关系(由get_ctx_gene得到的关系，客户挑选部分tf）
"""


def get_relation(infile):
    with open(infile) as f:
        all_relation = dict()
        for linno, line in enumerate(f, 1):
            if linno != 1:
                line = line.rstrip('\n')
                # print(line)
                tf, target = line.split('\t')
                if target not in all_relation.keys():
                    all_relation[target] = [tf]
                else:
                    all_relation[target].append(tf)
    # print(all_relation)
    return all_relation


def add_anno(raw_file, anno_file):
    out_file = raw_file.replace('.txt', '_anno.txt')
    all_relation = get_relation(anno_file)
    with open(raw_file) as f:
        with open(out_file, 'w') as f2:
            for linno, line in enumerate(f, 1):
                if linno == 1:
                    line_new = line.replace('\n', '\tanno\n')
                else:
                    target = line.split('\t')[0]
                    if target in all_relation.keys():
                        tf = all_relation[target]
                        tf = ','.join(tf)
                        line_new = line.replace('\n', f'\t{tf}\n')
                    else:
                        line_new = line.replace('\n', '\t\n')
                f2.write(line_new)


if __name__ == "__main__":
    need_anno = r'C:\Users\asus\Desktop\1\test2\GraphClust.AllMarkerGenes.txt'
    ctx_file = r'C:\Users\asus\Desktop\1\test2\CEBPB_MSX1_BHLHE40_TWIST.txt'
    add_anno(need_anno, ctx_file)
