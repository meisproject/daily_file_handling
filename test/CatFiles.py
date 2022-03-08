# coding:utf-8
import os
import xlwt
from filetype_convert.fileType_estimate import select_txt  # 列出该文件夹下的所有的txt


# 横向合并文件（只保留第一个的文件的第一列和第二列，其他文件只留第二列），输出文件为xls
def CatFiles(files, root):
    try:
        xls = xlwt.Workbook()  # 创建工作簿
        sheet = xls.add_sheet('sheet1', cell_overwrite_ok=True)
        firstfile = os.path.splitext(files[0])[0]  # 获取第一个文件的文件名
        firstInput = open(root + '\\' + files[0])
        xx = 1
        while True:
            firstLine = firstInput.readline()  # 逐行读入
            if not firstLine:  # 空行停止
                break
            firstItem1 = firstLine.split('\t')[0]
            if len(firstLine.split('\t')) > 1:
                firstItem2 = firstLine.split('\t')[1]
                try:
                    firstItem2 = float(firstItem2)
                except ValueError:
                    pass
            else:
                firstItem2 = ''
            sheet.write(xx, 0, firstItem1)  # x单元格经度，i+1 单元格纬度，输出内容
            sheet.write(xx, 1, firstItem2)  # x单元格经度，i+1 单元格纬度，输出内容
            xx += 1  # excel另起一行
        firstInput.close()
        sheet.write(0, 1, firstfile)

        i = 2
        for file in files:
            if files.index(file) != 0:  # 如果不是第一个文件，只留第二列信息
                try:
                    filename = os.path.splitext(file)[0]  # 获取文件名
                    inputFile = open(root + '\\' + file)
                    x = 1
                    while True:
                        line = inputFile.readline()  # 逐行读入
                        if not line:  # 空行停止
                            break
                        if len(line.split('\t')) > 1:
                            item = line.split('\t')[1]
                            try:
                                item = float(item)
                            except ValueError:
                                pass
                        else:
                            item = ''
                        sheet.write(x, i, item)  # x单元格经度，i+1 单元格纬度，输出内容
                        x += 1  # excel另起一行
                    inputFile.close()
                    sheet.write(0, i, filename)
                    i += 1  # excel另起一列
                except:
                    raise
        xls.save(root+ '\\AllSmaple.xls')
    except:
        raise


if __name__ == "__main__" :
    root = r"C:\Users\asus\Desktop\1\test2"
    files = select_txt(root)
    CatFiles(files, root)
