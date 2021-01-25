#coding:utf-8

x=[113.2,
171.147826086957,
217.06329113924,
281.728070175439,
350,
411.206896551724,
475.8]
y=[37.06,
44.4869565217391,
54.620253164557,
63.9473684210526,
73.8333333333333,
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
plt.ylim(0,100)
plt.legend(loc=0)
plt.savefig(fname="plottingAvgScores.pdf",format="pdf",bbox_inches='tight',pad_inches=0.05)