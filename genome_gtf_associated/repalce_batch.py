#! /usr/local/bin/python3
# coding:utf-8
# 根据NCBI的染色体对应表批量替换gff里的染色体名
import pandas as pd


def my_repalce(file, id_convert, result):
    id_result = pd.read_csv(id_convert, sep='\t')
    with open(result, 'w') as resu:
        try:
            f = open(file)
            while True:
                line = f.readline()  # 逐行读入
                if not line:  # 空行停止
                    break
                for i in range(0, len(id_result.index)):
                    line = line.replace(id_result.iloc[i, 0], id_result.iloc[i, 1])
                resu.writelines(line)
        except:
            raise


if __name__ == "__main__":
    inputfile = r"C:\Users\asus\Desktop\1\genome\GCA_000230245.1_ASM23024v1_genomic.gff"
    namefile = r'C:\Users\asus\Desktop\1\genome\染色体转化.txt'
    final = r'C:\Users\asus\Desktop\1\genome\GCA_000230245.1_ASM23024v1_genomic_new.gff'
    my_repalce(inputfile, namefile, final)

