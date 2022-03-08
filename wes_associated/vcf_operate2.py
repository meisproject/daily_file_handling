#! /usr/local/bin/python3
# coding:utf-8
# vcf转txt（一个位点的所有信息放在不同的行）
import glob
import os
import vcf  # PyVCF包


def print_title(vcf_file, txt):
    with open(txt, 'w') as f:
        f.writelines('CHROM\tPOS\tREF\tALT\t')
        for record in vcf_file:
            for sample in record.samples:
                f.writelines(sample.sample + '_DP' + '\t')
                f.writelines(sample.sample + '_RD' + '\t')
                f.writelines(sample.sample + '_AD' + '\t')
                f.writelines(sample.sample + '_FREQ' + '\t')
            f.writelines('\n')
            break


# samtools
def samtools_vcf2txt(vcf_file, txt):
    print_title(vcf_file, txt)
    with open(txt, 'a') as f:
        for record in vcf_file:
            if record.FILTER is None:
                chrom = str(record.CHROM)
                pos = str(record.POS)
                ref = str(record.REF)
                for i in range(0, len(record.ALT)):
                    alt = record.ALT[i]
                    if r'*' not in str(alt):
                        f.writelines(chrom + '\t' + pos + '\t' + ref + '\t' + str(alt) + '\t')
                        for sample in record.samples:
                            try:
                                if sample['DP'] is not None:
                                    f.writelines(str(sample['DP']) + '\t')
                                    alt_ad = sample['AD'][i + 1]
                                    f.writelines(str(sample['AD'][0]) + '\t' + str(alt_ad) + '\t')
                                    if alt_ad is not None:
                                        freq = alt_ad / sample['DP']
                                    else:
                                        freq = None
                                    f.writelines(str(freq) + '\t')
                                else:
                                    f.writelines(' \t \t \t \t')
                            except:
                                # print(sample.sample + chrom + pos + u'无信息')
                                continue
                        f.writelines('\n')


if __name__ == "__main__":
    path = r'C:\Users\asus\Desktop\1\test2'
    filelist = glob.glob(os.path.join(path, r'*.vcf'))  # glob类似于path.listdir，但是可以对文件进一步筛选
    for file in filelist:
        vcffile = vcf.Reader(filename=file)
        result = file.replace('.vcf', '.txt')
        samtools_vcf2txt(vcffile, result)
