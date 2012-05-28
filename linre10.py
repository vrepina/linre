
## plot eigen-values to select number of primary components
from numpy import load
in_st = load('out_big/linre9.0.out.npz')
eva_cnt = 60 #100
import matplotlib.pyplot as plt
for k in ((1,'0scatter'),(2,'1cov'),(3,'2corr')):
    eva = in_st[k[1]+'_eigval_best']
    plt.subplot(3,1,k[0])
    plt.semilogy(range(0,eva_cnt), eva[0:eva_cnt],'ro')
plt.show()