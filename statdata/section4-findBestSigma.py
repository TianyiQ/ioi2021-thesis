d=[0.568562930922061,
0.559522176625521,
0.497463604500593,
0.494656717311262,
0.493985129073224,
0.486095221127829,
0.415901480302441,
0.406945013021001,
0.405353176630375,
0.400130286529526,
0.3979498425997,
0.383822935577262,
0.378356369418552,
0.374611077789089,
0.370898991511755,
0.370044247924312,
0.348986199500662,
0.345514622304984,
0.344100613995208,
0.343385896981659,
0.340668948249654,
0.339714723757647,
0.33667798411033,
0.331446096871281,
0.330582752976709,
0.324977184077917,
0.320527682209059,
0.317324201936534,
0.305641983226307,
0.301049045320282,
0.299451899373743,
0.298860720930328,
0.294011099166842,
0.288692590853181,
0.281658918625775,
]
assert(len(d)==35)
tot=781

import math
from scipy.optimize import minimize

def R(x,sigma):
    sigma=abs(sigma)
    return (1+math.erf(x/(sigma*2)))/2
def logP(x,sigma):
    sigma=abs(sigma)
    return -x**2/(2*2*sigma**2)-math.log(2*math.pi**0.5*sigma)
def F(sigma):
    ret=math.log(R(d[-1],sigma))*(tot-len(d))
    for x in d:
        ret+=logP(x,sigma)
    return -ret

def getres(mthd):
    res=minimize(F,0.1,method=mthd,tol=1e-9,options={'disp': True})
    for i in range(1,1000):
        newres=minimize(F,math.exp(i/1000)-1,method=mthd,tol=1e-9)
        if newres.fun<res.fun:
            print(res.fun,newres.fun)
            res=newres
    return res

print(getres('BFGS').x)