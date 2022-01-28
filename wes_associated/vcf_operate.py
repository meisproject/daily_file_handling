#! /usr/local/bin/python3
# coding:utf-8
# vcf转txt（一个位点的所有信息放在一行）
import glob
import os
import vcf  # PyVCF包


def print_title(vcf_file, txt):
    with open(txt, 'w') as f:
        f.writelines('CHROM\tPOS\tREF\tALT\tFILTER\t')
        for record in vcf_file:
            for sample in record.samples:
                f.writelines(sample.sample + '_GT' + '\t')
                f.writelines(sample.sample + '_DP' + '\t')
                f.writelines(sample.sample + '_RD' + '\t')
                f.writelines(sample.sample + '_AD' + '\t')
                f.writelines(sample.sample + '_FREQ' + '\t')
            f.writelines('\n')
            break


# mutect2
def mutect2_vcf2txt(vcf_file, txt):
    print_title(vcf_file, txt)
    with open(txt, 'a') as f:  # a模式下追加写入
        for record in vcf_file:
            if len(record.FILTER) == 0:
                chrom = str(record.CHROM)
                pos = str(record.POS)
                ref = str(record.REF)
                alt = str(record.ALT)[1:-1]
                f.writelines(chrom + '\t' + pos + '\t' + ref + '\t' + alt + '\t' + 'PASS' + '\t')
                for sample in record.samples:
                    try:
                        f.writelines(sample['GT'] + '\t')
                        dp = 0
                        for ad in sample['AD']:
                            dp = dp + int(ad)
                        f.writelines(str(dp) + '\t')
                        alt_ad = str(sample['AD'][1:])
                        alt_ad = alt_ad.replace('[', '')
                        alt_ad = alt_ad.replace(']', '')
                        f.writelines(str(sample['AD'][0]) + '\t' + alt_ad + '\t')
                        freq = str(sample['AF']).replace('[', '')
                        freq = freq.replace(']', '')
                        f.writelines(freq + '\t')
                    except:
                        # print(sample.sample + chrom + pos + u'无信息')
                        continue
                f.writelines('\n')


# GATK
def gatk_vcf2txt(vcf_file, txt):
    print_title(vcf_file, txt)
    with open(txt, 'a') as f:
        for record in vcf_file:
            if record.FILTER is None:
                chrom = str(record.CHROM)
                pos = str(record.POS)
                ref = str(record.REF)
                alt = str(record.ALT)[1:-1]
                f.writelines(chrom + '\t' + pos + '\t' + ref + '\t' + alt + '\t' + '.' + '\t')
                for sample in record.samples:
                    try:
                        f.writelines(sample['GT'] + '\t')
                        if sample['GT'] != './.':
                            f.writelines(str(sample['DP']) + '\t')
                            alt_ad = str(sample['AD'][1:])
                            alt_ad = alt_ad.replace('[', '')
                            alt_ad = alt_ad.replace(']', '')
                            f.writelines(str(sample['AD'][0]) + '\t' + alt_ad + '\t')
                            # freq = list(map(lambda x: x/sample['DP'], sample['AD'][1:]))  # map对list内每一项运算，lambda隐式函数
                            freq = [ad / sample['DP'] for ad in sample['AD'][1:]]  # 列表生成式，作用和上一行一样
                            freq = str(freq).replace('[', '')
                            freq = freq.replace(']', '')
                            f.writelines(freq + '\t')
                        else:
                            # 如果基因型为./.，是没有突变的，把对应信息都用-表示
                            f.writelines('-' + '\t')
                            f.writelines('-' + '\t' + '-' + '\t')
                            f.writelines('-' + '\t')
                    except:
                        # print(sample.sample + chrom + pos + u'无信息')
                        continue
                f.writelines('\n')


# samtools
def samtools_vcf2txt(vcf_file, txt):
    print_title(vcf_file, txt)
    with open(txt, 'a') as f:
        for record in vcf_file:
            if record.FILTER is None:
                chrom = str(record.CHROM)
                pos = str(record.POS)
                ref = str(record.REF)
                alt = str(record.ALT)[1:-1]
                f.writelines(chrom + '\t' + pos + '\t' + ref + '\t' + alt + '\t' + '.' + '\t')
                for sample in record.samples:
                    try:
                        f.writelines(' \t')  # 没有GT信息
                        if sample['DP'] is not None:
                            f.writelines(str(sample['DP']) + '\t')
                            alt_ad = str(sample['AD'][1:])
                            alt_ad = alt_ad.replace('[', '')
                            alt_ad = alt_ad.replace(']', '')
                            f.writelines(str(sample['AD'][0]) + '\t' + alt_ad + '\t')
                            # freq = list(map(lambda x: x/sample['DP'], sample['AD'][1:]))  # map对list内每一项运算，lambda隐式函数
                            freq_list = []
                            for ad in sample['AD'][1:]:
                                if ad is not None:
                                    freq = ad / sample['DP']
                                else:
                                    freq = 'None'
                                freq_list.append(freq)
                            freq_list = str(freq_list).replace('[', '')
                            freq_list = freq_list.replace(']', '')
                            f.writelines(freq_list + '\t')
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
        with open(file) as vf:
            for line in vf:
                if r'Mutect' in line:
                    print(file + u'是Mutect2结果文件')
                    mutect2_vcf2txt(vcffile, result)
                    break
                elif r'HaplotypeCaller' in line:
                    print(file + u'是GATK结果文件')
                    gatk_vcf2txt(vcffile, result)
                    break
                elif r'samtoolsCommand=samtools' in line:
                    print(file + u'是Samtools结果文件')
                    samtools_vcf2txt(vcffile, result)
                    break

