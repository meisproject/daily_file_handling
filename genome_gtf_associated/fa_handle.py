#! /usr/local/bin/python3
# coding:utf-8
# 按照NCBI找到的染色体对照表更改fa的染色体名字

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import pandas as pd


def fa_handle(fa, name, output):
    id_result = pd.read_csv(name, sep='\t')
    records = SeqIO.parse(fa, "fasta")
    my_record = []
    for record in records:
        new_id = record.id.split(" ")[0]
        for i in range(0, len(id_result.index)):
            if id_result.iloc[i, 0] in new_id:
                new_id = new_id.replace(id_result.iloc[i, 0], id_result.iloc[i, 1])
            else:
                new_id = new_id
        my_seq = SeqRecord(record.seq, id=new_id, description="")
        my_record.append(my_seq)
        print(new_id)
    SeqIO.write(my_record, output, "fasta")


if __name__ == "__main__":
    f = r"C:\Users\asus\Desktop\1\GCF_000001635.27_GRCm39_genomic.fna"
    id_con = r"C:\Users\asus\Desktop\1\id转化表.txt"
    outfile = r"C:\Users\asus\Desktop\1\GCF_000001635.27_GRCm39_genomic_new.fna"
    fa_handle(f, id_con, outfile)

