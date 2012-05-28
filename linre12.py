
"""
Interactive explorer of flu;
use ',', '.', '[', ']' to through samples;
always visible em==ex peak;
peaks +-60 are observable with next values ~0;
its about to be a noise, we've marked it;
its possible to browse samples sorted by dis after pressing '/';
no facts was found found from this;
"""

sample_set = '2'

from numpy import load
l = load('linre_big'+sample_set+'.npz')
ema, exa, flum, expa, disa = l['ema'], l['exa'], l['flum'], l['expa'], l['disa']
X = flum.T

#mark errors
from linre_tools import find_peaks
X_err, X_wo_peaks = find_peaks(X,exa)
#X = X_wo_peaks

from linre_explorer import freq3d_explore
pga = [e+' '+str(d) for e, d in zip(expa,disa)]
is_sorted_by_dis = [False]
dis_idxa = list(enumerate(zip(expa,disa)))
dis_idxa.sort(key=lambda p:(p[1][0][0],p[1][1]))

def pg_indexer(i): return dis_idxa[i][0] if is_sorted_by_dis[0] else i
def on_key_inner(k): 
    if k == '/': is_sorted_by_dis[0] = not is_sorted_by_dis[0]
def mplot_inner(ax,gi):
    erra = X_err[gi]
    ax.plot(exa[erra],ema[erra],0,'ro')
    ax.set_zlabel ('Fluorescence')
    ax.set_zlim3d(-70,+70)
freq3d_explore(
    ema=ema, exa=exa, data=X, pga=pga, pg_indexer=pg_indexer,
    mplot_inner=mplot_inner, on_key_inner=on_key_inner
)