
n_components = 14

from numpy import load, array, where
from numpy.linalg import norm
from linre_tools import AttrDict
from persons import Persons
import matplotlib.pyplot as plt

l = AttrDict(load('linre_big'+'2'+'.npz'))

mds = AttrDict(load("out23/pred.npz"))
X, Y = mds.X, mds.Y
Ypred4n = mds.Ypred4n_components
Ym, Ypred = Y[:,0], Ypred4n[:,n_components-1]

eee = l.ema==l.exa
Xeee = X[:,eee]
#efm = Xeee.mean(axis=1)
#efm = [norm(s) for s in Xeee]
#efm = [len(where(s)[0]) for s in X_err]



#print Ym.shape, efm.shape
persons = Persons(mds.expa)
persons.plot( plt, efm, Ypred - Ym)
plt.show()