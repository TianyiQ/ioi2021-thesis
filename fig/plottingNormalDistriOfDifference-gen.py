d=[0.473045614952593,
0.447736468125885,
0.428985913357516,
0.420760369024789,
0.41515124352135,
0.405833793375885,
0.397526168918568,
0.394253238719156,
0.380917877188419,
0.330384285055802,
0.326863689244717,
0.327041417142448,
0.323839959911076,
0.321145648600365,
0.317525426500985,
0.316773847322366,
0.310774706528829,
0.307701107902387,
0.306279591776957,
0.305636809626806,
0.305085583722019,
0.300419285479095,
0.298809515219522,
0.295884244372572,
0.29218159873572,
0.289437474625885,
0.288242644225782,
0.28692067005731,
0.283844122914778,
0.282990704879198,
0.28017749282843,
0.274036119895761,
0.267471195712531,
0.259408710782269,
0.257203625892448
]

sigma=0.10895354

import numpy as np
import matplotlib.pyplot as plt
import math

def P(x):
    return math.exp(-x**2/(2*2*sigma**2))/(2*math.pi**0.5*sigma)

plt.rcParams['figure.figsize'] = (8.0, 4.0)
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rcParams['text.usetex']=False

nx=np.arange(-0.7,0.7,0.0005)
ny=np.empty_like(nx)
for i in range(len(nx)):
    ny[i]=P(nx[i])
plt.plot(nx,ny,'r',label='正态分布$N(0,2\\sigma^2)$',color='orange')
for x in d:
    plt.vlines(x,0,P(x),linewidth=0.5)

plt.xlabel('差值')
plt.ylabel('概率密度')
plt.ylim(0,P(d[-1]))
plt.xlim(-0.7,0.7)
plt.legend(loc=0)
plt.savefig(fname="plottingNormalDistriOfDifference.pdf",format="pdf")