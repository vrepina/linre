
"""
univariate linear model;
making cross-validation and selecting by best RMSEP;
RMSEP=0.5, ex=310, em=348;
so multivariate is better;
"""
#300,358?
group_count = 10

from numpy import load, savez, empty_like, empty, argmin
from scipy.stats import linregress
from sklearn.cross_validation import KFold
from linre_tools import AttrDict, RMSEP, BIAS, SE
from persons import Persons
import matplotlib.pyplot as plt

mds = AttrDict(load("out23/pred.npz"))
X, disa, expa = mds.X, mds.Y[:,0], mds.expa

var_count = X.shape[1]
ma = empty((var_count,))
disa_pred4var = empty_like(X)
for varn in range(var_count):
    Xc = X[:,varn]
    loo = KFold( n=len(disa), k=group_count, indices=False )
    for fit, test in loo:
        slope, intercept, r_value, p_value, stderr = linregress(Xc[fit],disa[fit])
        disa_pred4var[test,varn] = Xc[test] * slope + intercept
    ma[varn] = RMSEP(disa,disa_pred4var[:,varn])

ia = argmin(ma)
print ma[ia]
l = AttrDict(load('linre_big2.npz'))
print l.exa[ia], l.ema[ia]

persons = Persons(expa)
Ymm = [0,max(disa)]
plt.plot(Ymm,Ymm,'g-')
persons.plot(plt,disa,disa_pred4var[:,ia])
plt.title('Univariate, K-Fold, '+str(len(disa))+' samples')
plt.xlabel('IS, measured, mg/L')
plt.ylabel('IS, predicted, mg/L')
plt.savefig("out26/pred.png")


Ym, Ypred = disa, disa_pred4var[:,ia]
print 'RMSEP',  RMSEP(Ym, Ypred)
print 'BIAS', BIAS(Ym, Ypred)
print 'SE', SE(Ym, Ypred)
savez('out26/pred.npz',Ym=Ym,Ypred=Ypred,expa=expa)