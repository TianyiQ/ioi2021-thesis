#coding:utf-8

import math
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (8.0, 4.0)
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

x=[0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95]
y=[7861/26907,7066/26907,5950/26907,5093/26907,4517/26907,3994/26907,3503/26907,3054/26907,2572/26907,2003/26907,1475/26907,1133/26907,751/26907,439/26907,278/26907]
assert(len(x)==len(y))

def calcpre(x):
    return x*np.log(x)-x
def func(x, a):
    ret=np.empty_like(x)
    for i in range(len(x)):
        ret[i]=(calcpre(x[i]+0.05)-calcpre(x[i]-0.05))*a
    return ret
X=np.array(x)
Y=np.array(y)
from sympy import *
xx=Symbol('x',real=True)
a=1/integrate(log(xx),(xx,0.2,1)).evalf()
print(a) # -2.09156
plot1 = plt.plot(x, y, 's',label='邻近区间内人数占比',color='blue')
nx=np.arange(0.2, 0.95, 0.001)
ny=func(nx,a)
plot2 = plt.plot(nx,ny, 'r',label='邻近区间内对数曲线线下面积',color='orange')
plt.xlabel('分数')
plt.ylabel('人数占比')
plt.legend(loc=0)
plt.savefig(fname="fittingNoipScores.pdf",format="pdf")
sqrdif=0
for i in range(len(x)):
    sqrdif+=(y[i]-func(x,a)[i])**2
print(sqrdif)