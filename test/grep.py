filedir = r'C:\Users\asus\Desktop\1\RSC'
want = r'metabolism.txt'
allInt = r'SelectedNormalizedCounts.txt'
result = r'Marcrophage_metabolism.txt'

# 读取要提取的内容
wantfile = open(filedir + '\\' + want)
lines = []
while True:
    wantline = wantfile.readline().rstrip()  # 逐行读入
    if not wantline:  # 空行停止
        break
    lines.append(wantline)
wantfile.close()

# 读取所有内容
allfile = open(filedir + '\\' + allInt)
alllines = []
while True:
        allline = allfile.readline()
        if not allline:  # 空行停止
            break
        alllines.append(allline)
allfile.close()

# 判断并写出
resultfile = open(filedir + '\\' + result, 'w')
for line in lines:
    for newline in alllines:
        if line in newline:
            resultfile.writelines(newline)
        else:
            continue
resultfile.close()
