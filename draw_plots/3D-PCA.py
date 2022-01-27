# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from sklearn import decomposition, datasets


'''
centers = [[1, 1], [-1, -1], [1, -1]]
iris = datasets.load_iris()  # 导入鸢尾花数据
X = iris.data  # 获取每个样本信息（每行一个样本，4个属性）
y = iris.target  # 获取每个样本品种（总共3种）

fig = plt.figure(figsize=(5.5, 3))  # 创建窗口，固定大小
ax = Axes3D(fig, rect=[0, 0, .7, 1], elev=48, azim=134)  # 出现3D网格

pca = decomposition.PCA(n_components=3)  # 降到3维
pca.fit(X)  # 求得训练集X的均值，方差，最大值，最小值等这些训练集X固有的属性
X = pca.transform(X)  # 在Fit的基础上，进行标准化，降维，归一化等操作，具体看工具

labelTups = [('Setosa', 0), ('Versicolour', 1), ('Virginica', 2)]  # 将数字分类和品种名对应起来
for name, label in labelTups:  # 加上品种标签
    ax.text3D(X[y == label, 0].mean(),
              X[y == label, 1].mean() + 1.5,
              X[y == label, 2].mean(), name,
              horizontalalignment='center',
              bbox=dict(alpha=.5, edgecolor='w', facecolor='w'))
# Reorder the labels to have colors matching the cluster results
y = np.choose(y, [1, 2, 0]).astype(np.float)  # astype修改数据类型；choose按照y的数字作为下标对[1,2,0]进行筛选
sc = ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=y, cmap="Spectral", edgecolor='k')  # 按照降维后的数据，按照品种作为颜色分类，画点

ax.w_xaxis.set_ticklabels([])  # 去除坐标轴标签
ax.w_yaxis.set_ticklabels([])
ax.w_zaxis.set_ticklabels([])

colors = [sc.cmap(sc.norm(i)) for i in [1, 2, 0]]
custom_lines = [plt.Line2D([], [], ls="", marker='.',
                mec='k', mfc=c, mew=.1, ms=20) for c in colors]
ax.legend(custom_lines, [lt[0] for lt in labelTups],  # 加上legend
          loc='center left', bbox_to_anchor=(1.0, .5))

plt.show()
'''

# centers = [[1, 1], [-1, -1], [1, -1]]
filename = r'C:\Users\asus\Desktop\1\All.fpkm.txt'
# y = list(range(0, 6))  # 分组情况
y = np.repeat(range(0, 3), 3)
data = np.genfromtxt(filename, dtype=str)  # 采用numpy以str格式读入列表
sample = data[0][1:]  # 样本名
transpose_data = np.transpose(data[1:])  # 对读入数据进行转置
transpose_data = transpose_data[1:].astype(float)  # 基因表达数据，转为浮点数

fig = plt.figure(figsize=(7, 7))  # 创建窗口，固定大小
ax = Axes3D(fig, rect=[0, 0, .9, .9], elev=25, azim=134)  # 出现3D网格，elev和azim是改变视角用的

pca = decomposition.PCA(n_components=3)  # 降到3维
pca.fit(transpose_data)  # 求得训练集X的均值，方差，最大值，最小值等这些训练集X固有的属性
X = pca.transform(transpose_data)  # 在Fit的基础上，进行降维

x_max = max(abs(X[:, 0]))  # 找到所有样本中X、Y、Z绝对值最大的数
y_max = max(abs(X[:, 1]))
z_max = max(abs(X[:, 2]))

sc = ax.scatter(X[:, 0]/x_max, X[:, 1]/y_max, X[:, 2]/z_max, c=y, cmap="Set1", edgecolor='k', s=45)  # 按照降维后的数据画点

for i in range(0, len(sample)):
    textc = ax.text3D((X[i, 0] + x_max*0.1)/x_max, (X[i, 1] + y_max*0.1)/y_max, (X[i, 2] + z_max*0.1)/z_max, sample[i],
                      horizontalalignment='center', verticalalignment='center', fontsize=12,
                      bbox=dict(alpha=.4, edgecolor='w', facecolor='w'))
ax.w_xaxis.set_label_text('PC1')
ax.w_yaxis.set_label_text('PC2')
ax.w_zaxis.set_label_text('PC3')

plt.show()

