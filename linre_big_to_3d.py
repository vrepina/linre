
from numpy import load
from linre_tools import AttrDict
from linre_explorer import freq3d_save

for fn in ['linre_big','linre_big2']:
    l = AttrDict(load(fn+'.npz'))
    freq3d_save(fn,
        ema=l.ema, exa=l.exa, data=l.flum.T, pga=l.expa, zlabel='Fluorescence'
    )
