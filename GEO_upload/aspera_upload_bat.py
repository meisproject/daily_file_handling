#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
# 生成windows下利用aspera上传数据至NCBI的bat文件
# 使用bat前需要保证aspera已经配置好环境变量
# 大致思路是，每个样本按序上传，如果上传不成功，errorlevel返回值不会是0，则重新上传对应的文件
import os
import glob


def get_upload_bat(need_upload, ssh_file, max_speed, outfile):
    files = glob.glob(os.path.join(need_upload, r'**'))
    with open(os.path.join(outfile, r'aspera_upload.bat'), 'w') as f:
        f.writelines(r'echo off' + '\n')
        f.writelines('\n')
        flag = 0
        for eve_file in files:
            eve_file_path = os.path.join(need_upload, eve_file)
            flag = flag + 1
            f.writelines(r':file' + str(flag) + '\n')
            f.writelines(r'ascp -i ' + ssh_file + r' -QT -l' + str(max_speed) + 'm -k1 ' +
                         eve_file_path + ' asp-sra@upload.ncbi.nlm.nih.gov:incoming' + '\n')
            f.writelines(r'if errorlevel 0 (' + '\n')
            f.writelines(r'echo ' + eve_file + ' 上传成功' + '\n')
            if flag < len(files):
                f.writelines(r'goto file' + str(flag + 1) + '\n')
            f.writelines(r') else (' + '\n')
            f.writelines(r'echo ' + eve_file + ' 上传失败，重新上传' + '\n')
            f.writelines(r'goto file' + str(flag) + '\n')
            f.writelines(r')' + '\n')
            f.writelines(r'pause' + '\n')
            f.writelines('\n')


if __name__ == "__main__":
    # fastq_path是存放需要上传的.fastq.gz的路径
    fastq_path = r'E:\zhangchao\张潮老师-10个样本20200106-10X-5-Novaseq-human-姗姗上传3'
    # ssh_pos是aspera上传的密钥的路径
    ssh_pos = r'C:\Users\asus\Desktop\1\test\sra-1.ssh.priv'
    # out_path是bat文件输出路径
    out_path = r'C:\Users\asus\Desktop\1\test'
    # speed是上传限制的最大速度(M/s)
    speed = 25
    get_upload_bat(fastq_path, ssh_pos, speed, out_path)
