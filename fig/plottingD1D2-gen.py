import math
import numpy as np
import numpy.matlib
import numpy.linalg
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import scipy.integrate as integrate

sigmaF=0.10895354*(2**0.5)
sigmaA=0.078188270041128
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

def Ex(mu,sigma=sigmaA):
    return integrate.quad((lambda s:(R(s-mu,sigma)*C(s))),0,1)[0]

def Med(mu,sigma=sigmaA):
    return integrate.quad(C,mu,1)[0]

plt.rcParams['figure.figsize'] = (8.0, 4.0)
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rcParams['text.usetex']=False

nx=np.arange(0.01,1,0.01)
ny_ex=np.empty_like(nx)
ny_ex_rel=np.empty_like(nx)
ny_med=np.empty_like(nx)
ny_med_rel=np.empty_like(nx)
nc=np.empty_like(nx)
for i in range(len(nx)):
    nc[i]=C(nx[i])
    V=integrate.quad(X,nx[i],1)[0]
    ny_ex[i]=Ex(nx[i])-V
    ny_ex_rel[i]=ny_ex[i]/V
    ny_med[i]=Med(nx[i])-V
    ny_med_rel[i]=ny_med[i]/V
# plt.plot(nx,nc,'r',label='分数分布',color='green',linestyle='--')
plt.plot(nx,ny_ex,'r',label='$D_1$关于$\\mu$的图像',color='red',linestyle='--')
# plt.plot(nx,ny_ex_rel,'r',label='$D_1/V$关于$\\mu$的图像',color='red')
plt.plot(nx,ny_med,'r',label='$D_2$关于$\\mu$的图像',color='blue',linestyle='--')
# plt.plot(nx,ny_med_rel,'r',label='$D_2/V$关于$\\mu$的图像',color='blue')
plt.xlabel('$\\mu$')
plt.ylabel('差值')
plt.legend(loc=0)
plt.xlim(0,1)
plt.gca().xaxis.set_major_locator(MultipleLocator(0.1))
plt.grid(linestyle='--')
plt.savefig(fname="plottingD1D2.pdf",format="pdf",bbox_inches='tight',pad_inches=0.05)