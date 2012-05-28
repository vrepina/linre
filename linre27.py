
"""
pls: coefs explorer
"""

from itertools import groupby
from numpy import load, array, hstack
from linre_tools import AttrDict
from linre_explorer import freq3d_save
import matplotlib.pyplot as plt

l = AttrDict(load('linre_big.npz'))
ema, exa = l.ema, l.exa

def load_pls(preprocess):
    pls = AttrDict(load("out21/"+preprocess+"loadings.npz"))
    return ( pls.coefs, pls.x_mean[:,None], pls.y_mean )

def show3d(preprocess):
    coefs, x_mean, y_mean = load_pls(preprocess)
    print y_mean
    data = hstack((coefs, x_mean)).T
    pga = ['coefs','x_mean']
    freq3d_save("out27/a"+preprocess,ema=ema,exa=exa,data=data,pga=pga) #not final plot

def plot_slices(fn,data):
    subplot_index = 0
    share = dict()
    plt.figure(figsize=(32,16))
    for ex,grp in groupby(enumerate(exa),lambda p:p[1]):
        ia = array([p[0] for p in grp])
        subplot_index += 1
        share['sharey'] = plt.subplot(6,6,subplot_index,**share)
        plt.axis([200,800,-1,1])
        plt.grid(True)
        plt.title(ex)
        plt.plot(ema[ia],data[ia])
    plt.savefig("out27/"+fn+"slices.pdf")
    plt.savefig("out27/"+fn+"slices.png")
    plt.cla()

def plot_slices4model(preprocess):
    coefs, x_mean, y_mean = load_pls(preprocess)
    plot_slices(preprocess+'coefs_',coefs)
    plot_slices(preprocess+'x_mean_',x_mean)


for preprocess in ['','pp_']: 
    plot_slices4model(preprocess)
    show3d(preprocess)