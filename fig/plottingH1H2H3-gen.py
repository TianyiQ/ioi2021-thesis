costs=[1.9854540490170365,1.8897541219398266,1.783125960258785,1.697661177237779,1.5833520920472837,1.499519431563351,1.3999052841943496,1.299999325270233]
x1s=[0.11394000787380809,0.1552115117282269,0.20341885780262836,0.23489489080820136,0.2850241829465864,0.3243740272124554,0.38111643418482016,0.4486791582817367,]
x2s=[0.3616143710651146,0.35727851169949304,0.3588230683776886,0.3796779340021746,0.4059465485621914,0.43086125275598436,0.4589843750741278,0.49046097762175916,]
x3s=[0.5336339315602933,0.533633931821313,0.5336339304450538,0.5336339101399719,0.5336330310173099,0.5336205377222956,0.5333756468004085,0.5297378279288261,]

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

def getvec_x(x,tss):
    allprob=rangeR(0-x,1-x)
    once_x=np.arange(rP/2,1,rP,dtype=np.float64)
    once_h=P2(once_x-x)/allprob
    assert(abs(sum(once_h)-1)<1e-8)
    cur_h=once_h.copy()
    ret=[]
    for i in range(len(tss)):
        ncP=cP*(i+1)
        nrP=1/ncP
        cur_x=np.arange(nrP/2,1,nrP,dtype=np.float64)
        assert(len(cur_h)==len(cur_x))
        t=tss[i]
        d=np.searchsorted(cur_x,t-nrP/2,side='right')
        cur_h[:d]=0
        ret.append(sum(cur_h))
        if d<len(cur_h):
            cur_h[d]*=((cur_x[d]+nrP/2)-t)/nrP
        if i<len(tss)-1:
            cur_h=signal.convolve(cur_h,once_h)
            cur_h=(np.append([0],cur_h)+np.append(cur_h,[0]))/2
    return np.array(ret)

# mp=dict([])

def getvec(tss):
#     print(tss[2])
#     if tuple(tss) in mp:
#         return mp[tuple(tss)]
    ret=integrate.quad_vec((lambda x:getvec_x(x,tss)*X(x)),0,1,epsabs=1e-8,epsrel=1e-8)[0]
#     mp[tuple(tss)]=ret
    return ret

plt.rcParams['figure.figsize'] = (9.0, 9.0)
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rcParams['text.usetex']=False

plta=plt.subplot(2,1,1)
pltb=plt.subplot(2,1,2)

plta.plot(costs,x1s,'s-',label='第1轮分数线',color='darkblue')#,markerfacecolor='none')
plta.plot(costs,x2s,'s-',label='第2轮分数线',color='blue')#,markerfacecolor='none')
plta.plot(costs,x3s,'s-',label='第3轮分数线',color='cornflowerblue')#,markerfacecolor='none')
tmp=[getvec([x1s[i],x2s[i],x3s[i]]) for i in range(len(costs))]
tmp1=[f[0] for f in tmp]
tmp2=[f[1] for f in tmp]
tmp3=[f[2] for f in tmp]
pltb.plot(costs,tmp1,'^-',label='第1轮选拔人数',color='darkgreen')#,markerfacecolor='none')
pltb.plot(costs,tmp2,'^-',label='第2轮选拔人数',color='forestgreen')#,markerfacecolor='none')
pltb.plot(costs,tmp3,'^-',label='第3轮选拔人数',color='limegreen')#,markerfacecolor='none')
# plt.vlines(costs,[min(x1s[i],tmp3[i]) for i in range(len(x1s))],[max(x3s[i],tmp1[i]) for i in range(len(x1s))],linestyles='dotted',colors='orange',linewidths=1.5)
# plt.legend(aa,['x1','x2','x3'],loc=0)
# plt.legend(bb,['r1','r2','r3'],loc=0)
plta.vlines(costs,x1s,x3s,linestyles='dotted',colors='orange',linewidths=1.5)
plta.legend(loc=0)
plta.grid(linestyle='--')
plta.set_xlabel('开销')
plta.set_ylabel('分数')
plta.set_ylim((0,None))
pltb.vlines(costs,tmp3,tmp1,linestyles='dotted',colors='orange',linewidths=1.5)
pltb.legend(loc=0)
pltb.grid(linestyle='--')
pltb.set_xlabel('开销')
pltb.set_ylabel('人数（占初始人数的比例）')
pltb.set_ylim((0,None))
plt.savefig(fname="plottingH1H2H3.pdf",format="pdf",bbox_inches='tight',pad_inches=0.05)