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
OXint=integrate.quad(OX,0,1)[0]
X=lambda x:(OX(x)/OXint)

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
    assert(abs(sum(once_h)-1)<1e-8)
    cur_h=once_h.copy()
    ret_prob=0
    ret_sum=0
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

def getvec(tss):
    ret=integrate.quad_vec((lambda x:getvec_x(x,tss)*X(x)),0,1,epsabs=1e-8,epsrel=1e-8)[0]
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

TT=2 # to be assigned with T

def testok2(**kwargs):
    tss=kwargs["x_new"]
    return np.min(tss)>=0 and np.max(tss)<=1 and totprob2(tss)>=0.1-1e-8 and cost2(tss)<=TT

result = optimize.differential_evolution((lambda x:-ex2(x)),bounds=[(0,1),(0,1)],constraints=[optimize.NonlinearConstraint(totprob2,0.1-1e-8,1),optimize.NonlinearConstraint(cost2,0,TT)],tol=1e-6) # tol should be chosen carefully
print(result)
print(totprob2(result.x),ex2(result.x),cost2(result.x))
getvec2(result.x,show=True) # display h1,h2,h3