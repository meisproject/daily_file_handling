# coding:utf-8
import xlrd

# source是单个基因，target是逗号分隔的多个基因，都改成1对1

data = xlrd.open_workbook(r'C:\Users\asus\Desktop\1\Human Peripheral blood.xls')
outfile = r'C:\Users\asus\Desktop\1\result.txt'
out = open(outfile, 'w')
table = data.sheets()[0]
for i in range(table.nrows-1):
    source = table.cell(i, 0).value
    targets = table.cell(i, 1).value.split(',')
    for target in targets:
        out.writelines(source + '\t' + target + '\n')
out.close()
