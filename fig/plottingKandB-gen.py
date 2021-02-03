import math
import numpy as np
from numpy.core.numerictypes import ScalarType
import numpy.matlib
import numpy.linalg
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from matplotlib import cm
import scipy.integrate as integrate
from scipy.optimize import curve_fit

sigmaF=0.10895354*(2**0.5)
sigmaA=0.078188270041128
sigmaA2=sigmaA*(2**0.5)
gamma=0.5488594815581366
thres=0.103468491232405

# OX=lambda x:1.6971354708*(x-1)**2
OX=lambda x:(1.6971354708*x**2 + -3.3520704577*x + 1.6552008479)
OXint=integrate.quad(OX,0,1)[0]
X=lambda x:(OX(x)/OXint)
newA=1.6971354708/OXint

def R(x,sigma=sigmaA):
    return (math.erf(x/(2**0.5*sigma))+1)/2

def omR(x,sigma=sigmaA):
    return (1-math.erf(x/(2**0.5*sigma)))/2

def rangeR(l,r,sigma=sigmaA):
    return 1-R(l,sigma)-omR(r,sigma)

def P(x,sigma=sigmaA):
    return np.exp(-(x**2)/(2*sigma**2))/((2*math.pi)**0.5*sigma)

def C(x,sigma=sigmaA):
    if sigma==0:
        return X(x)
    return integrate.quad((lambda s:(X(s)*P(x-s,sigma)/rangeR(0-s,1-s,sigma))),0,1)[0]

def Ex(mu,oldsigma=sigmaA,newsigma=sigmaA):
    totsigma=np.sqrt(oldsigma**2+newsigma**2)
    return integrate.quad((lambda x:(R(x-mu,totsigma)*X(x))),0,1)[0]

plt.rcParams['figure.figsize'] = (8.0, 4.0)
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rcParams['text.usetex']=False

# try to fit C (C>0.7) for fixed sigma

def funcarr(x,b,cura):
    # print(x,b,e)
    return [cura*(max(0,b-cx)**2) for cx in x]

low=0.6
highsig=0.4
allx=np.arange(low,1,0.0025)
ally=np.arange(0,highsig,0.005)
lenx,leny=len(allx),len(ally)

def getcoe(sigma):
    ys=[C(allx[i],sigma) for i in range(lenx)]
    ret,tmp=curve_fit(funcarr,allx,ys,p0=[1,newA],bounds=([1,0],[np.inf,np.inf]))
    return ret

K=[]
B=[]
curs=[]
tots=[]
for i in range(leny):
    coescur=getcoe(ally[i]*(2**-0.5))
    coesano=getcoe(ally[i])
    curs.append(coesano)
    tots.append(coescur)
    B.append(coescur[1]*(coescur[0]-coesano[0])/3)
    K.append(coescur[1]/coesano[1])
    # K.append(coesano[1])
    # B.append(coesano[0])

def fun(k,b):
    # kx+b<x, k>1 b<0
    # (k-1)x<-b, x<-b/(k-1)
    if k<=1:
        return 1
    return min(1,-b/(k-1))

worstfun=[]
for i in range(leny):
    coesano=curs[i]
    worstfun.append(1)
    for coescur in curs[0:i]+[tots[i]]:
        cb=coescur[1]*(coescur[0]-coesano[0])/3
        ck=coescur[1]/coesano[1]
        worstfun[i]=min(worstfun[i],fun(ck,cb))

plt.plot([ally[i] for i in range(leny)],[K[i] for i in range(leny)],'r',color='blue',label='一次项系数关于$\\sigma$的图像（典型情况）')
plt.plot([ally[i] for i in range(leny)],[B[i] for i in range(leny)],'r',color='red',label='常数项关于$\\sigma$的图像（典型情况）')
plt.plot([ally[i] for i in range(leny)],[fun(K[i],B[i]) for i in range(leny)],'r',color='orange',linestyle='--',label='使一次函数值小于自变量的最大自变量取值（典型情况）')
plt.plot([ally[i] for i in range(leny)],worstfun,'r',color='green',linestyle='--',label='使一次函数值小于自变量的最大自变量取值（最坏情况）')
plt.xlabel('$\\sigma$')
plt.ylabel('值')
plt.xlim(0,highsig)
plt.ylim((None,1.8))
plt.grid(linestyle='--')
plt.legend(loc=0)
plt.gca().yaxis.set_major_locator(MultipleLocator(0.2))
# plt.show()
plt.savefig(fname="plottingKandB.pdf",format="pdf",bbox_inches='tight',pad_inches=0.05)