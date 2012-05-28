
"""
trying the pcr
"""
samples_in_testing_set = 5
n_components = 14

from numpy import load, arange, where
from linre_tools import find_peaks, PCA
from scipy.linalg import lstsq 

l = load('linre_big.npz')
flum = l['flum']
disa = l['disa']
exa = l['exa']
expa = l['expa']

X_orig = flum.T
X_err, X_orig = find_peaks(X_orig,exa)

## exclude outliers
PC = PCA(n_components=2).fit_transform(X_orig.copy()) #mean inside
PC1 = PC[:,0]
good_std = PC1 < PC1.std()

a4fit = arange(len(X_orig)) >= samples_in_testing_set
ia4fit, = where( a4fit & good_std )
X4fit = X_orig[ia4fit,:]
disa4fit = disa[ia4fit]
pca = PCA(n_components=n_components)
PC = pca.fit_transform(X4fit.copy())
dis_mean = disa4fit.mean()
#print PC.shape,(disa4fit-dis_mean).shape
(a,residues,rank,s) = lstsq(PC,disa4fit-dis_mean)

PC = pca.transform(X_orig.copy())
mdis = PC.dot(a[:,None])[:,0] + dis_mean

from persons import Persons
persons = Persons(expa)

import matplotlib.pyplot as plt
plt.figure()
dis_max = max(disa)
plt.plot([0,dis_max],[0,dis_max],'g-')
persons.plot(plt,disa,where(mdis<dis_max+1,where(mdis<-1,-1,mdis),dis_max+1))
plt.show()
