import math
import numpy as np
import numpy.matlib
import numpy.linalg
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import scipy.integrate as integrate

sigmaF=0.10895354*(2**0.5)
sigmaA=0.078188270041128
sigmaA2=sigmaA*(2**0.5)
gamma=0.5488594815581366
thres=0.103468491232405

OX=lambda x:(1.6971354708*x**2 + -3.3520704577*x + 1.6552008479)
OXint=integrate.quad(OX,0,1)[0]
X=lambda x:(OX(x)/OXint)

def R(x,sigma=sigmaA):
    return (math.erf(x/(2**0.5*sigma))+1)/2

def omR(x,sigma=sigmaA):
    return (1-math.erf(x/(2**0.5*sigma)))/2

def rangeR(l,r,sigma=sigmaA):
    return 1-R(l,sigma)-omR(r,sigma)

def P(x,sigma=sigmaA):
    return np.exp(-(x**2)/(2*sigma**2))/((2*math.pi)**0.5*sigma)

def C(x):
    return integrate.quad((lambda s:(X(s)*P(x-s)/rangeR(0-s,1-s))),0,1)[0]

def Ex(mu,totsigma=sigmaA2):
    return integrate.quad((lambda x:(R(x-mu,totsigma)*X(x))),0,1)[0]

def Med(mu,totsigma=sigmaA):
    return integrate.quad((lambda x:(R(x-mu,totsigma)*X(x))),0,1)[0]

plt.rcParams['figure.figsize'] = (8.0, 5.0)
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rcParams['text.usetex']=False

nx=np.arange(0.01,1,0.0025)
ny_ex=np.empty_like(nx)
ny_ex_rel=np.empty_like(nx)
ny_med=np.empty_like(nx)
ny_med_rel=np.empty_like(nx)
nc=np.empty_like(nx)
for i in range(len(nx)):
    nc[i]=C(nx[i])
    V=integrate.quad(X,nx[i],1)[0]
    ex=Ex(nx[i])
    med=Med(nx[i])
    ny_ex[i]=ex-V
    ny_ex_rel[i]=ny_ex[i]/ex
    ny_med[i]=med-V
    ny_med_rel[i]=ny_med[i]/med
# plt.plot(nx,nc,'r',label='分数分布',color='green',linestyle='--')
fig=plt.figure()
ax=fig.add_subplot(1,1,1)
ax2=ax.twinx()
ax.plot(nx,ny_ex,'r',label='$D_1$关于$\\mu$的图像',color='red',linewidth=1)
ax2.plot(nx,ny_ex_rel,'r',label='$D_1/\\mathrm{E}[U_p]$关于$\\mu$的图像',linestyle='--',color='red',linewidth=1)
ax.plot(nx,ny_med,'r',label='$D_2$关于$\\mu$的图像',color='blue',linewidth=1)
ax2.plot(nx,ny_med_rel,'r',label='$D_2/\\mathrm{Med}[U_p]$关于$\\mu$的图像',linestyle='--',color='blue',linewidth=1)
ax.set_xlabel('$\\mu$')
ax.set_ylabel('绝对差值')
ax.legend(loc='upper left')
ax2.set_ylabel('相对差值')
ax2.legend(loc='lower right')
ax.set_xlim(0,1)
ax.set_ylim(-0.025,+0.05)
ax2.set_ylim(-0.5,+1)
# ax2.set_xlim(0,1)
plt.gca().xaxis.set_major_locator(MultipleLocator(0.1))
plt.hlines(0,0,1,colors='black',linestyles='--',linewidth=1)
# plt.grid(linestyle='--')
plt.savefig(fname="plottingD_1D_2.pdf",format="pdf",bbox_inches='tight',pad_inches=0.05)