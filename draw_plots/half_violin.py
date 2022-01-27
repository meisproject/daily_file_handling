#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
plotnine的教程
半个violin加boxplot加散点
"""
import numpy as np
import pandas as pd
import pandas.api.types as pdtypes

from plotnine import *
from plotnine.data import *

np.random.seed(123)
n = 20
mu = (1, 2.3)
sigma = (1, 1.6)

before = np.random.normal(loc=mu[0], scale=sigma[0], size=n)
after = np.random.normal(loc=mu[1], scale=sigma[1], size=n)

df = pd.DataFrame({
    'value': np.hstack([before, after]),
    'when': np.repeat(['before', 'after'], n),
    'id': np.hstack([range(n), range(n)])
})

df['when'] = df['when'].astype(pdtypes.CategoricalDtype(categories=['before', 'after']))
df.head()


def alt_sign(x):
    """Alternate +1/-1 if x is even/odd"""
    return (-1) ** x


lsize = 0.65
fill_alpha = 0.7
shift = 0.1

m1 = aes(x=stage('when', after_scale='x+shift*alt_sign(x)'))  # shift outward
m2 = aes(x=stage('when', after_scale='x-shift*alt_sign(x)'), group='id')  # shift inward

(ggplot(df, aes('when', 'value', fill='when'))
 + geom_violin(m1, style='left-right', alpha=fill_alpha, size=lsize, show_legend=False)
 + geom_point(m2, color='none', alpha=fill_alpha, size=2, show_legend=False)
 + geom_line(m2, color='gray', size=lsize, alpha=0.6)
 + geom_boxplot(width=shift, alpha=fill_alpha, size=lsize, show_legend=False)
 + scale_fill_manual(values=['dodgerblue', 'darkorange'])
 + theme_classic()
 + theme(figure_size=(8, 6))
 ).draw(show=True)

# 保存图片用ggplot.save()
