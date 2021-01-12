d=[0.473045614952593,
0.447736468125885,
0.428985913357516,
0.420760369024789,
0.41515124352135,
0.405833793375885,
0.397526168918568,
0.394253238719156,
0.380917877188419,
0.330384285055802,
0.326863689244717,
0.327041417142448,
0.323839959911076,
0.321145648600365,
0.317525426500985,
0.316773847322366,
0.310774706528829,
0.307701107902387,
0.306279591776957,
0.305636809626806,
0.305085583722019,
0.300419285479095,
0.298809515219522,
0.295884244372572,
0.29218159873572,
0.289437474625885,
0.288242644225782,
0.28692067005731,
0.283844122914778,
0.282990704879198,
0.28017749282843,
0.274036119895761,
0.267471195712531,
0.259408710782269,
0.257203625892448
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

print(abs(getres('BFGS').x)) # 0.10895354