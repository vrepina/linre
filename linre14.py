
"""
loadings plot;
shows, how flu on different freq-s affect PC;
axis: em, ex, loading; figure per PC; ',' and '.' goes to next PC;
lines should be smooth, so that flu on next freq-s affect PC in similar way;
but they are not in large areas; there is an error;
then we disable normalizing (/=std) data, and lines become smooth;
scaling can prevent spectroscopic interpretation of loadings;
we see peaks on em==ex; is it right, or we'd preprocess data in this area?
idea: may be we'd normalize not by var (freq pair), but by em or ex;
"""
normalize=0

from numpy import load, array, arange
from linre_tools import pcs_calc
from linre_explorer import freq3d_save
l = load('linre_big.npz')
max_components = 7
pco = pcs_calc(
    exa=l['exa'], flum=l['flum'], max_components=max_components,
    no_peaks=1,  recalc_wo_outliers=1, normalize=normalize,
    ret_loadings=1,
)
freq3d_save('out14/loadings',
    ema=l['ema'], exa=l['exa'], data=pco.loadings, zlabel='Scaling coefficient',
    pga=['L'+str(i+1) for i in range(max_components)]
)

