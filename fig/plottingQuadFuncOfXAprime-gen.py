import numpy as np
xs=np.arange(0.004,1.001,0.002)
polys=[1.6971354708*x**2 + -3.3520704577*x + 1.6552008479 for x in xs]

from matplotlib import pyplot as plt

plt.rcParams['figure.figsize'] = (8.0, 4.0)
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

plt.plot(xs, polys, 'r',label='二次函数图像',color='orange')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(linestyle='--')
plt.xlim(0,1)
plt.legend(loc=0)
plt.savefig(fname="plottingQuadFuncOfXAprime.pdf",format="pdf",bbox_inches='tight',pad_inches=0.05)