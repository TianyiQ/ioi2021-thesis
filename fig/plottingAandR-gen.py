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
def func(x,b,e,cura):
    # print(x,b,e)
    e=2
    return cura*(max(0,b-x)**e)

def funcarr(x,b,e,cura):
    # print(x,b,e)
    e=2
    return [cura*(max(0,b-cx)**e) for cx in x]

low=0.6
highsig=0.4
allx=np.arange(low,1,0.0025)
ally=np.arange(0,highsig,0.005)
lenx,leny=len(allx),len(ally)
Vforx=[integrate.quad(X,x,1)[0] for x in allx]
nz=np.empty((leny,lenx)) # rel
ex=np.empty((leny,lenx))
allx,ally=np.meshgrid(allx,ally)
print(allx.shape,ally.shape)
for i in range(leny):
    for j in range(lenx):
        nz[i,j]=C(allx[i,j],ally[i,j])

coes=[]
for i in range(leny):
    xs=[allx[i,j] for j in range(lenx)]
    ys=[nz[i,j] for j in range(lenx)]
    coes.append(0)
    coes[i],tmp=curve_fit(funcarr,xs,ys,p0=[1,2,newA],bounds=([1,1,0],[np.inf,np.inf,np.inf]))
    # print(i,coes[i][0],coes[i][1],coes[i][2])

plt.plot([ally[i,0] for i in range(leny)],[coes[i][0] for i in range(leny)],'r',color='blue',label='r关于$\\sigma$的图像')
plt.plot([ally[i,0] for i in range(leny)],[coes[i][2] for i in range(leny)],'r',color='red',label='a关于$\\sigma$的图像')
plt.xlabel('$\\sigma$')
plt.ylabel('函数值')
plt.xlim(0,highsig)
plt.grid(linestyle='--')
plt.legend(loc=0)
plt.savefig(fname="plottingAandR.pdf",format="pdf",bbox_inches='tight',pad_inches=0.05)