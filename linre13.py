
"""
PCA score plot
(1)
    we see A4 and A6 samples are very far from others;
    in linre12.py very high peaks are seen there;
    m. b. samples are bad;
    A5 dis is missing, they are next to it;
    even before taking dis into account we see it only using PCA;
(2) 
    we exclude A4 and A6 and get plot without outliers;
    sample color groups along the PC(-s);
(3) 
    we go through all steps with normalized data and peaks-rounded
    (in the first case they was just centered);
    about the same result;
    very nice color groups;
    decide later weather to normalize data;
    E1 is a bit far from other samples on a set of plots;
    in linre12.py it has highest peak on em==ex;
    can't find clear reason to drop it, so keep it;
"""


from numpy import array
from linre_tools import pcs_calc, take_good, AttrDict

def plot_scores(nm,pc4axis,PC,PC_std,expa,annotate=1):
    PC_x, PC_y = PC[:,array(pc4axis)].T
    PC_x_std, PC_y_std = PC_std[array(pc4axis)]
    import matplotlib.pyplot as plt
    plt.title('PCA, '+str(len(PC_y))+' samples')
    plt.xlabel('T'+str(pc4axis[0]+1))
    plt.ylabel('T'+str(pc4axis[1]+1))
    plt.plot(
        (PC_x_std,PC_x_std,-PC_x_std,-PC_x_std,PC_x_std),
        (PC_y_std,-PC_y_std,-PC_y_std,PC_y_std,PC_y_std),
        'r'
    )
    from persons import Persons
    Persons(expa).plot(plt,PC_x, PC_y)
    dfn = "out13/"+nm
    plt.savefig(dfn+".png")
    plt.savefig(dfn+".pdf")
    plt.cla()

from numpy import load

l = load('linre_big.npz')
opt = AttrDict(
    exa=l['exa'], flum=l['flum'], max_components=7,
    ret_PC=1, ret_PC_std=1, ret_good_idxa=1,
)

def fix_expa(d):
    d.expa = take_good(l['expa'],d)
    del d['good_idxa']
    return d

pco = fix_expa(pcs_calc(no_peaks=0,normalize=0,recalc_wo_outliers=0,**opt))
plot_scores('1',(0,1),**pco)

from itertools import combinations
comb = list(combinations(range(opt.max_components), 2))

pco = fix_expa(pcs_calc(no_peaks=0,normalize=0,recalc_wo_outliers=1,**opt))
for pair in comb: plot_scores("2_"+str(pair[0])+"_"+str(pair[1]),pair,**pco)

pco = fix_expa(pcs_calc(no_peaks=1,normalize=1,recalc_wo_outliers=1,**opt))
for pair in comb: plot_scores("3_"+str(pair[0])+"_"+str(pair[1]),pair,**pco)
