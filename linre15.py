"""
residuals plot by variables (ex-em);

"""
max_components = 9

from numpy import load, array, arange, power, sqrt
from linre_tools import pcs_calc
from linre_explorer import freq3d_save
l = load('linre_big.npz')
pco = pcs_calc(
    exa=l['exa'], flum=l['flum'], max_components=max_components,
    no_peaks=1,  recalc_wo_outliers=1, normalize=0,
    ret_X=1, ret_pca=1, ret_PC=1
)
def evar(X_fwd,X_back): return power(X_fwd-X_back,2).sum(axis=0) ## variance
X = pco.X
var0 = evar( X, X.mean(axis=0) ) ## mean in already 0
var = evar( X, pco.pca.inverse_transform(pco.PC) )
freq3d_save('out15/residuals',
    ema=l['ema'], exa=l['exa'], data=sqrt(var/var0)[None], pga=['residuals'] 
) #sqrt(var/var0)
print pco.pca.explained_variance_ratio_

