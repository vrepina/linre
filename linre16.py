"""
residuals plots by samples;
axis: sample number, (un)explained variance for sample;
relative seems to be more convenient;
more components explaine more;
can show candidates for drop;
"""

max_components = 10

from numpy import load, power, arange
from linre_tools import pcs_calc, take_good

l = load('linre_big.npz')
import matplotlib.pyplot as plt
from persons import Persons
def evar(e): return power(e,2).sum(axis=1) ## variance for samples

for n in arange(max_components)+1:
    pco = pcs_calc(
        exa=l['exa'], flum=l['flum'], max_components=n,
        no_peaks=1, recalc_wo_outliers=1, normalize=0,
        ret_X=1, ret_pca=1, ret_good_idxa=1, ret_PC=1
    )
    X_reconstructed = pco.pca.inverse_transform(pco.PC);
    expa = take_good(l['expa'],pco)
    xa = arange(len(expa))
    vara_orig = evar( pco.X )
    vara_unexplained = evar( pco.X - X_reconstructed )
    vara_explained = evar( X_reconstructed )
    def plot(explained,rel,vara):
        Persons(expa).plot(plt,xa,vara)
        plt.savefig("out16/%s%s%s.png" % (rel,n,explained))
        plt.cla()
    plot('u','abs',vara_unexplained)
    plot('e','abs',vara_explained)
    plot('u','rel',vara_unexplained / vara_orig)
    ## (vara_unexplained / vara_orig)+(vara_explained / vara_orig) == 1
    
