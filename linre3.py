#3D/2D Eex/em/correlation
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from itertools import groupby
from scipy.stats import pearsonr, spearmanr
from freq_pairs import load

def plot_it(res,filename_part):
    fig = plt.figure(figsize=(32,16))
    ax = Axes3D(fig) #,azim=100)
    ax.scatter([p.em for p in res],[p.ex for p in res],[p.corr for p in res])
    ax.set_xlabel('EM, nm')
    ax.set_ylabel('EX, nm')
    ax.set_zlabel('R, ' + filename_part)
    plt.savefig("out/e-%s-3d.png" % filename_part)

    subplot_index = 0
    share = dict()
    plt.figure(figsize=(32,16))
    for ex,grp in groupby(res,lambda p:p.ex):
        res4ex = list(grp)
        subplot_index += 1
        share['sharey'] = plt.subplot(6,6,subplot_index,**share)
        plt.axis([200,800,-1,1])
        plt.grid(True)
        plt.title(ex)
        plt.plot([p.em for p in res4ex],[p.corr for p in res4ex])
    plt.savefig("out/e-%s-slices.png" % filename_part)

(dis_list,res, exp_list) = load('linre_big.st')
res.sort(key=lambda p:(p.ex,p.em))
for p in res: p.corr = pearsonr(dis_list,p.flu)[0]
plot_it(res,'pearson')
for p in res: p.corr = spearmanr(dis_list,p.flu)[0]
plot_it(res,'spearman')

