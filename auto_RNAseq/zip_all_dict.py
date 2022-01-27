#! /usr/local/bin/python3
# coding:utf-8
"""
批量压缩文件夹下的所有子文件夹（只会压缩路径下的子文件夹，文件不会单独压缩）
"""
import zipfile
import os
import time


def zip_all_dict(path):
    """

    :param path: 需要压缩的子文件夹所在的上级路径
    """
    os.chdir(path)
    all_dicts = os.listdir(path)
    for each_dict in all_dicts:
        each_dict_abs = os.path.join(path, each_dict)
        if os.path.isdir(each_dict_abs):
            zip_file = each_dict + '.zip'
            with zipfile.ZipFile(zip_file, 'w') as f:
                for ro, di, fi in os.walk(each_dict):
                    for each_file in fi:
                        try:
                            f.write(os.path.join(ro, each_file))
                        except OSError as my_error:
                            print(f'{os.path.join(ro, each_file)} 出错，错误为{my_error}')
            print(f'{zip_file}压缩完成')


if __name__ == "__main__":
    my_path = r'F:\1.梅姗姗_第二批\164.齐雪娇_人_单细胞（脑脊液）\齐雪娇老师单细胞项目结果（LBYY-20210526-scRNA-QXJ-SH）交付2022.01.20'
    start_time = time.time()
    zip_all_dict(my_path)
    print(f'所有文件夹都压缩好了，耗时{(time.time() - start_time)/60}分钟')
