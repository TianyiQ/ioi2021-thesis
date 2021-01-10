d=[0.568562930922061,
0.559522176625521,
0.497463604500593,
0.494656717311262,
0.493985129073224,
0.486095221127829,
0.415901480302441,
0.406945013021001,
0.405353176630375,
0.400130286529526,
0.3979498425997,
0.383822935577262,
0.378356369418552,
0.374611077789089,
0.370898991511755,
0.370044247924312,
0.348986199500662,
0.345514622304984,
0.344100613995208,
0.343385896981659,
0.340668948249654,
0.339714723757647,
0.33667798411033,
0.331446096871281,
0.330582752976709,
0.324977184077917,
0.320527682209059,
0.317324201936534,
0.305641983226307,
0.301049045320282,
0.299451899373743,
0.298860720930328,
0.294011099166842,
0.288692590853181,
0.281658918625775,
]

sigma=0.12223922

import numpy as np
import matplotlib.pyplot as plt
import math

def P(x):
    return math.exp(-x**2/(2*2*sigma**2))/(2*math.pi**0.5*sigma)

plt.rcParams['figure.figsize'] = (8.0, 4.0)
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rcParams['text.usetex']=False

nx=np.arange(-0.8,0.8,0.0005)
ny=np.empty_like(nx)
for i in range(len(nx)):
    ny[i]=P(nx[i])
plt.plot(nx,ny,'r',label='正态分布$N(0,2\\sigma^2)$',color='orange')
for x in d:
    plt.vlines(x,0,P(x),linewidth=0.8)

plt.xlabel('差值')
plt.ylabel('概率密度')
plt.ylim(0,0.6)
plt.legend(loc=0)
plt.savefig(fname="plottingNormalDistriOfDifference.pdf",format="pdf")