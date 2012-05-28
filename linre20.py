
#PC0 ???, use TRVP/EVRP?

from numpy import array, load, savez, sqrt, power, arange
from linre_tools import AttrDict, RMSEP, BIAS, SE
import matplotlib.pyplot as plt

#sample_set, sample_count = '', 69
sample_set, sample_count = '2', 141
#sample_set, sample_count = '2', 10

l = AttrDict(**load('out18/ts'+sample_set+'g1k'+str(sample_count)+'.npz'))
disa, disa_pred4n_components, expa = l.disa, l.disa_pred4n_components, l.expa

x4plot = arange(len(disa_pred4n_components))+1
y4plot_1 = []
#y4plot_2 = []
pce = []
for a, disa_pred in enumerate(disa_pred4n_components):
    e_sq_sum = power((disa_pred-disa),2).sum(axis=0)
    #RMSEP = sqrt( e_sq_sum / len(disa) )
    #y4plot_1.append(RMSEP)
    TRVP = e_sq_sum / len(disa)
    EVRP = e_sq_sum / power(disa,2).sum(axis=0)
    #y4plot_2.append(EVRP)
    correcting = pce[0]*0.01*a if a else 0
    #pce.append(correcting+EVRP)
    pce.append(correcting+TRVP)
    
#plt.plot(x4plot,y4plot_1)
#plt.plot(x4plot,y4plot_2,'r-')
plt.plot(x4plot,pce,'r-')
plt.title('PCA') #, correction
plt.xlabel('PC Count')
#plt.ylabel('RMSEP, mg/L')
plt.savefig('out20/co.png')

#Min[Vytot_val_PC[0]*0.01*a + Vytot_val_PC[a]]
#n 15
for n in [7,14,15,16]:
    Ym, Ypred = disa, disa_pred4n_components[n-1]
    print 'PCA',n
    print 'RMSEP',  RMSEP(Ym, Ypred)
    print 'BIAS', BIAS(Ym, Ypred)
    print 'SE', SE(Ym, Ypred)
    savez('out20/pca'+str(n)+'pred.npz',Ym=Ym,Ypred=Ypred,expa=expa)