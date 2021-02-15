import math
import numpy as np
import numpy.matlib
import numpy.linalg
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from matplotlib import cm
import scipy
import scipy.integrate as integrate
import scipy.optimize as optimize
from scipy import special
from scipy import signal

sigmaF=0.10895354*(2**0.5)
sigmaA=0.078188270041128
# sigmaA2=sigmaA*(2**0.5)
gamma=0.5488594815581366
# thres=0.103468491232405

OX=lambda x:(1.6971354708*x**2 + -3.3520704577*x + 1.6552008479)
INTOX=lambda x:(1.6971354708*x**3/3 + -3.3520704577*x**2/2 + 1.6552008479*x)
OXint=integrate.quad(OX,0,1)[0]
X=lambda x:(OX(x)/OXint)
INTX=lambda x:(INTOX(x)/OXint)

def R(x,sigma=sigmaA):
    return (special.erf(x/(2**0.5*sigma))+1)/2

def omR(x,sigma=sigmaA):
    return (1-special.erf(x/(2**0.5*sigma)))/2

def rangeR(l,r,sigma=sigmaA):
    return 1-R(l,sigma)-omR(r,sigma)

def P(x,sigma=sigmaA):
    return np.exp(-(x**2)/(2*sigma**2))/((2*math.pi)**0.5*sigma)

def C(x):
    return integrate.quad((lambda s:(X(s)*P(x-s)/rangeR(0-s,1-s))),0,1)[0]

cP=256
rP=1/cP

def P2(x):
    return rangeR(x-rP/2,x+rP/2)

def getvec_x(x,tss): # prob,probx,sum
    allprob=rangeR(0-x,1-x)
    once_x=np.arange(rP/2,1,rP,dtype=np.float64)
    once_h=P2(once_x-x)/allprob
#     print(sum(once_h))
    assert(abs(sum(once_h)-1)<1e-8)
    cur_h=once_h.copy()
    ret_prob=0
    ret_sum=0
#     once_h2=signal.convolve(once_h,[0.5,0.5])
    for i in range(len(tss)):
        ncP=cP*(i+1)
        nrP=1/ncP
        cur_x=np.arange(nrP/2,1,nrP,dtype=np.float64)
        assert(len(cur_h)==len(cur_x))
        t=tss[i]
        ret_sum+=np.sum(cur_h)
        d=np.searchsorted(cur_x,t-nrP/2,side='right')
        cur_h[:d]=0
        if d<len(cur_h):
            cur_h[d]*=((cur_x[d]+nrP/2)-t)/nrP
        if i<len(tss)-1:
            cur_h=signal.convolve(cur_h,once_h)
            cur_h=(np.append([0],cur_h)+np.append(cur_h,[0]))/2
#             cur_h=cur_h[0::2]+(np.append(cur_h[1::2],[0])+np.append([0],cur_h[1::2]))/2
#             cur_h=(curh[0::2]+np.append([0],curh[0::2]))/2+(curh[1::2]+6*np.append([0],curh[1::2])+np.append([0,0],curh[1::2]))/8
#             cur_h=(np.append(signal.convolve(cur_h[0::2],once_h[0::2]),[0])+np.append([0],signal.convolve(cur_h[1::2],once_h[1::2])))*2
    ret_prob=np.sum(cur_h)
    return np.array([ret_prob,ret_prob*x,ret_sum])

# mp=dict([])

def getvec(tss):
#     print(tss[2])
#     if tuple(tss) in mp:
#         return mp[tuple(tss)]
    ret=integrate.quad_vec((lambda x:getvec_x(x,tss)*X(x)),0,1,epsabs=1e-8,epsrel=1e-8)[0]
#     mp[tuple(tss)]=ret
    return ret

def totprob(tss):
    r=getvec(tss)
    return r[0]

def ex(tss):
    r=getvec(tss)
    return r[1]/r[0]

def cost(tss):
    r=getvec(tss)
    return r[2]

mp=dict([])

lastrt=0

def getvec2(tss,show=False):
    global lastrt
    if (tuple(tss) in mp) and not show:
        return mp[tuple(tss)]
    tss=list(tss)
    if totprob(tss+[0])<0.1+1e-9:
        mp[tuple(tss)]=getvec(tss+[0])
        return mp[tuple(tss)]
    tmp=scipy.optimize.root_scalar(lambda x:totprob(tss+[x])-0.1, bracket=[0,1], method='brentq',xtol=1e-9)
    rt=tmp.root
    if show:
        lastrt=rt
        print(tss+[rt])
    mp[tuple(tss)]=getvec(tss+[rt])
    return mp[tuple(tss)]

def totprob2(tss):
    r=getvec2(tss)
    return r[0]

def ex2(tss):
    r=getvec2(tss)
    return r[1]/r[0]

def cost2(tss):
    r=getvec2(tss)
    return r[2]

plt.rcParams['figure.figsize'] = (8.0, 4.0)
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rcParams['text.usetex']=False

ax2=plt.subplot(1,1,1)
ax=ax2.twinx()
xs=np.arange(0,1,0.01)
xx=[0.11394000787380809, 0.3616143710651146, 0.5336339315602933]
ys=[getvec_x(cx,xx)[0] for cx in xs]
print(sum(xs[i]*ys[i]*X(xs[i]) for i in range(len(xs)))/sum(ys[i]*X(xs[i]) for i in range(len(xs))))
ax.plot(xs,ys,color='blue',label='$P(x)$的图像',linestyle='--')
# ax.vlines(ex(xx),-10,10,colors='orange',linestyles='dotted',linewidths=1.5)
# at=scipy.optimize.root_scalar(lambda x:INTX(x)-0.9, bracket=[0,1], method='brentq',xtol=1e-9).root
# mnv=scipy.integrate.quad(lambda x:X(x)*x,at,1)[0]/0.1
# ax.vlines(mnv,-10,10,colors='red',linestyles='dotted',linewidths=1.5)
ax.set_ylim(0-0.05,1+0.05)
ax.set_xlim(0,1)
ax.set_ylabel('通过概率')
ax.legend(loc=(0.8,0.3))
ax2.plot(xs,X(xs),color='red',label='$\\mathcal{X}_{A_1}(x)$的图像')
ax2.plot(xs,[X(cx)*getvec_x(cx,xx)[0] for cx in xs],color='orange',label='$P(x)\\cdot\\mathcal{X}_{A_1}(x)$的图像')
ax2.set_ylabel('分布密度')
ax2.set_xlabel('期望得分')
ax2.legend(loc=(0.01,0.3))
# getvec2([0],show=True)
# xx=[0]+[lastrt]
# ys=[getvec_x(cx,xx)[0] for cx in xs]
# print(sum(xs[i]*ys[i]*X(xs[i]) for i in range(len(xs)))/sum(ys[i]*X(xs[i]) for i in range(len(xs))))
# plt.plot(xs,ys)
plt.savefig(fname="plottingDistriInOptimizedArrangement.pdf",format="pdf",bbox_inches='tight',pad_inches=0.05)