
"""
pls: loadings explorer

loadings are like cutten, what about making EX even less?

higher component: more noise

"""

preprocess = 'pp_' #|''

from numpy import load, hstack
from linre_tools import AttrDict
from linre_explorer import freq3d_save

l = AttrDict(load('linre_big.npz'))
pls = AttrDict(load("out21/"+preprocess+"loadings.npz"))

#print pls.y_loadings, l.ema.shape, l.exa.shape, pls.x_loadings.shape

def annotate(pf,d): return map(lambda v:pf+str(v), range(d))

data = hstack((pls.x_loadings,pls.x_rotations)).T
pga = annotate('L ',pls.x_loadings.shape[1]) + annotate('R ',pls.x_rotations.shape[1])

print pga

freq3d_save("out22/"+preprocess+"loadings",ema=l.ema,exa=l.exa,data=data,pga=pga)
