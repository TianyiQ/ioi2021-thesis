#coding:utf-8

x=[183.142857142857,
224.128571428571,
244.471074380165,
287.447619047619,
345.655737704918,
401.965517241379,
475.1]
y=[37.4285714285714,
45.0571428571429,
54.8347107438017,
64.0857142857143,
73.7704918032787,
83.3793103448276,
93.5]

import numpy as np
import matplotlib.pyplot as plt
import math
plt.rcParams['figure.figsize'] = (8.0, 4.0)
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plot1 = plt.plot(x, y, 's-',label='分数段内的平均分',color='blue')
plt.xlabel('复赛均分')
plt.ylabel('初赛均分')
plt.legend(loc=0)
plt.savefig(fname="plottingAvgScores.pdf",format="pdf")