#coding:utf-8

x=[-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,0.6,0.7]
y=[0/440,6/440,9/440,19/440,41/440,46/440,52/440,82/440,64/440,52/440,36/440,22/440,8/440,3/440,0/440]

import numpy as np
import matplotlib.pyplot as plt
import math
plt.rcParams['figure.figsize'] = (8.0, 4.0)
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
from scipy.optimize import curve_fit
def presum(x,a):
    return (math.erf(x*a)+1)/2
def func(x,a):
    ret=np.empty_like(x)
    for i in range(len(ret)):
        ret[i]=presum(x[i]+0.05,a)-presum(x[i]-0.05,a)
    return ret
X=np.array(x)
Y=np.array(y)
coe,tmp=curve_fit(func,X,Y)
a=coe[0]
print(coe)
yvals=func(X,a)
plot1 = plt.plot(x, y, 's',label='邻近区间内人数占比',color='blue')
nx=np.arange(-0.7,0.7,0.01)
ny=func(nx,a)
plot2 = plt.plot(nx,ny, 'r',label='邻近区间内正态分布曲线线下面积',color='orange')
plt.xlabel('分数偏移量')
plt.ylabel('人数占比')
plt.legend(loc='lower center') #指定legend的位置右下角
# plt.title('curve_fit'))
plt.savefig(fname="fittingOffsets.pdf",format="pdf")