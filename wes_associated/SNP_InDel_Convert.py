#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
# 挑出每个位点每个样本突变率最高的情况，孙彦阔项目
import os
import glob
import vcf  # PyVCF包


def convert(path, file):
    vcffile = vcf.Reader(filename=os.path.join(path, file))
    result = os.path.join(path, file).replace('.vcf', '.txt')
    with open(result, 'a') as f:
        # 写title
        f.writelines('CHROM\tPOS\tREF\t')
        for record in vcffile:
            for sample in record.samples:
                f.writelines(sample.sample + '_Alt' + '\t')
                f.writelines(sample.sample + '_DP' + '\t')
                f.writelines(sample.sample + '_RD' + '\t')
                f.writelines(sample.sample + '_AD' + '\t')
                f.writelines(sample.sample + '_FREQ' + '\t')
            f.writelines('\n')
            break
        # 写内容
        for record in vcffile:
            if record.FILTER is None and str(record.ALT) != '[<*>]':
                chrom = str(record.CHROM)
                pos = str(record.POS)
                ref = str(record.REF)
                f.writelines(chrom + '\t' + pos + '\t' + ref + '\t')
                for sample in record.samples:
                    if sample['DP'] is None:
                        f.writelines(' \t \t \t \t \t')
                    else:
                        try:
                            alt_ad_raw = sample['AD'][1:]
                            alt_ad = list(filter(None, sample['AD'][1:]))  # 过滤空值
                            if len(alt_ad) > 0:
                                ad_max = alt_ad.index(max(alt_ad))
                                alt_max = record.ALT[alt_ad_raw.index(max(alt_ad))]
                                f.writelines(str(alt_max) + '\t')
                                f.writelines(str(sample['DP']) + '\t')
                                f.writelines(str(sample['AD'][0]) + '\t' + str(alt_ad[ad_max]) + '\t')
                                freq = alt_ad[ad_max] / sample['DP']
                                f.writelines(str(freq) + '\t')
                            else:
                                f.writelines(' \t \t \t \t \t')
                        except:
                            continue
                f.writelines('\n')


if __name__ == "__main__":
    inpath = r'F:\1.梅姗姗_第二批\32.孙彦阔_PCR产物\备份\4.CallVariantion\1.RawVCF'
    filelist = glob.glob(os.path.join(inpath, r'*.vcf'))  # glob类似于path.listdir，但是可以对文件进一步筛选
    for infile in filelist:
        convert(inpath, infile)
