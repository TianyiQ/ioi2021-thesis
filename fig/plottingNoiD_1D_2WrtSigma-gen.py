import math
import numpy as np
import numpy.matlib
import numpy.linalg
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from matplotlib import cm
import scipy.integrate as integrate

sigmaF=0.10895354*(2**0.5)
sigmaA=0.078188270041128
sigmaA2=sigmaA*(2**0.5)
gamma=0.5488594815581366
thres=0.7

def R(x,sigma=sigmaA):
    return (math.erf(x/(2**0.5*sigma))+1)/2

def omR(x,sigma=sigmaA):
    return (1-math.erf(x/(2**0.5*sigma)))/2

def rangeR(l,r,sigma=sigmaA):
    return 1-R(l,sigma)-omR(r,sigma)

def P(x,sigma=sigmaA):
    return np.exp(-(x**2)/(2*sigma**2))/((2*math.pi)**0.5*sigma)

OX=lambda x:((1.6971354708*x**2 + -3.3520704577*x + 1.6552008479)*omR(thres-x))
OXint=integrate.quad(OX,0,1)[0]
X=lambda x:(OX(x)/OXint)

def C(x):
    return integrate.quad((lambda s:(X(s)*P(x-s)/rangeR(0-s,1-s))),0,1)[0]

def Ex(mu,oldsigma=sigmaA,newsigma=sigmaA):
    totsigma=np.sqrt(oldsigma**2+newsigma**2)
    return integrate.quad((lambda x:(R(x-mu,totsigma)*X(x))),0,1)[0]

plt.rcParams['figure.figsize'] = (8.0, 5.0)
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rcParams['text.usetex']=False

allx=np.arange(0.02,1,0.005)
ally=np.arange(0.02,0.2,0.005)
lenx,leny=len(allx),len(ally)
Vforx=[integrate.quad(X,x,1)[0] for x in allx]
nz=np.empty((leny,lenx)) # rel
allx,ally=np.meshgrid(allx,ally)
print(allx.shape,ally.shape)
for i in range(leny):
    for j in range(lenx):
        ex=Ex(allx[i,j],newsigma=ally[i,j])
        # print(ex-Vforx[j],ex)
        nz[i,j]=(ex-Vforx[j])/ex
        # print(nz[i,j])
for i in range(1,leny):
    for j in range(lenx):
        nz[i,j]-=nz[0,j]
for j in range(lenx):
    nz[0,j]=0
partmin=1
for i in range(1,leny):
    for j in range(lenx):
        if allx[i,j]>0.5:
            partmin=min(partmin,nz[i,j])
print(partmin)
fig=plt.figure()
ax=fig.add_subplot(111,projection='3d')
ax.plot_surface(allx,ally,nz,cmap=cm.coolwarm)#.reversed())
ax.contour(allx,ally,nz,offset=-0.3,zdir='z',cmap=cm.coolwarm)#.reversed())
# ax.plot_surface(allx,ally,np.empty_like(nz),cmap='rainbow')
ax.set_xlabel('$\\mu$')
ax.set_ylabel('$\\sigma$')
ax.set_zlabel('相对差值随$\\sigma$的增量')#,labelpad=9.5)
ax.set_xlim(0,1)
ax.set_ylim(0.2,0)
ax.set_zlim(min(-0.3,np.min(nz)),np.max(nz))
ax.yaxis.set_major_locator(MultipleLocator(0.06))
ax.zaxis.set_major_locator(MultipleLocator(0.1))
# plt.hlines(0,0,1,colors='black',linestyles='-',linewidth=0.5)
plt.savefig(fname="plottingNoiD_1D_2WrtSigma.pdf",format="pdf",bbox_inches='tight',pad_inches=0.05)