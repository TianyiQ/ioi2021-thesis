sigma=0.10895354
thres=0.103468491232405

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import scipy.integrate as integrate
import math

def R(x):
    return (1+math.erf(x/(sigma*2)))/2

def F(x):
    return -math.log(x)/R(x-thres)

plt.rcParams['figure.figsize'] = (8.0, 5.0)
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rcParams['text.usetex']=False

nx=np.arange(0.001,1,0.0005)
ny=np.empty_like(nx)
ny2=np.empty_like(nx)
ny0=np.empty_like(nx)
tot=integrate.quad(F,0,1)
print(tot)
print(1/tot[0])
for i in range(len(nx)):
    ny[i]=F(nx[i])
    ny0[i]=ny[i]/tot[0]
    ny2[i]=-math.log(nx[i])
plt.plot(nx,ny,'r',label='完整分数分布（比例未调整）',color='red')
plt.plot(nx,ny0,'r',label='完整分数分布（比例已调整）',color='orange')
plt.plot(nx,ny2,'r',label='原始分数分布',linestyle='--',color='blue')
plt.xlabel('分数')
plt.ylabel('密度')
plt.legend(loc=0)
plt.ylim(0,6)
plt.xlim(0,1)
plt.gca().xaxis.set_major_locator(MultipleLocator(0.1))
plt.grid(linestyle='--')
plt.savefig(fname="plottingNewNoipScores.pdf",format="pdf",bbox_inches='tight',pad_inches=0.05)