import math
import numpy as np
import numpy.matlib
import numpy.linalg
import matplotlib.pyplot as plt

sigmaF=0.10895354*(2**0.5)
sigmaA=0.078188270041128
gamma=0.5488594815581366
thres=0.103468491232405

def R(x,sigma=sigmaA):
    return (math.erf(x/(2**0.5*sigma))+1)/2

def omR(x,sigma=sigmaA):
    return (1-math.erf(x/(2**0.5*sigma)))/2

def rangeR(l,r,sigma=sigmaA):
    return 1-R(l,sigma)-omR(r,sigma)

def P(x,sigma=sigmaA):
    return np.exp(-(x**2)/(2*sigma**2))/((2*math.pi)**0.5*sigma)

def C(x):
    return gamma*(-np.log(x))/omR(thres-x,sigma=sigmaF)

CNT=500
IV=1/CNT
xs=np.arange(IV,1-IV/2,IV)
assert(len(xs)==CNT-1)
ys=np.empty_like(xs)
for i in range(len(xs)):
    ys[i]=C(xs[i])
A=np.matlib.zeros((len(xs),len(xs)))
# for i in range(len(xs)):
#     print(xs[i],P(xs[i]))
for i in range(len(xs)):
    ss=0
    for j in range(len(xs)):
        vi=(i+1)*IV
        vj=(j+1)*IV
        A[i,j]=P(vi-vj)/rangeR(0-vi,1-vi)*IV # contribution of i to j
        ss+=A[i,j]
        
from cvxopt import solvers, matrix 
P=np.matlib.zeros((len(xs),len(xs)))
q=np.matlib.zeros((len(xs),1))
base=0
for i in range(len(xs)):
    val=1
    coes=[]
    for j in range(len(xs)):
        coes.append(A[j,i]/ys[i])
    # (val-sum coes*X)**2
    base+=val**2
    for j in range(len(xs)):
        q[j]-=coes[j]*val*2
        for k in range(len(xs)):
            P[j,k]+=coes[j]*coes[k]
            P[k,j]+=coes[j]*coes[k]

from sympy import binomial

k=3 # level
G=np.matlib.zeros((len(xs)-k+len(xs),len(xs)))
for i in range(len(xs)-k):
    for j in range(k+1):
        G[i,i+j]=(-1)**(j+1)*binomial(k,j)
for i in range(len(xs)):
    G[i+len(xs)-k,i]=-1
h=np.matlib.zeros((len(xs)-k+len(xs),1))

print('start solver')

import scipy.optimize
def cost(x):
    x=np.mat(x)
    return np.matmul(np.matmul(x,P),x.T)[0,0]/2+np.matmul(x,q)[0,0]
sol=scipy.optimize.minimize(fun=cost,x0=[C((i+1)*IV) for i in range(len(xs))],method='trust-constr',
                            constraints=scipy.optimize.LinearConstraint(G,-np.inf,0),options={'maxiter':100000})
# result written in sol.x
print(sol,file=open('section4-quadProgSol.txt','a')) 
print(sum(sol.x))