

from numpy import load, mean
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.backends.backend_agg import FigureCanvasAgg
from persons import Persons
from linre_tools import AttrDict, RMSEP, BIAS, SE

class SharingFigure:
    def __init__(self):
        self.figure = Figure(figsize=(12,12))
        self.share = AttrDict(dict())
        self.canvas = FigureCanvasAgg(self.figure)
    def subplot(self,pos):
        ax = self.figure.add_subplot(pos,**(self.share))#2,1,axes=ax
        self.share.sharey = ax
        self.share.sharex = ax
        return ax
    def save(self,fn): self.canvas.print_figure(fn,bbox_inches='tight')

share = AttrDict(dict())
def inc(fn,title,do_plot=0,eyl=1):
    l = AttrDict(load(fn+"pred.npz"))
    Ym, Ypred, expa = l.Ym, l.Ypred, l.expa
    print title
    print 'RMSEP',RMSEP(Ym, Ypred), 'BIAS',BIAS(Ym, Ypred), 'SE',SE(Ym, Ypred)
    #print len(Ym),len(Ypred),len(expa)
    if not do_plot: return
    persons = Persons(expa)
    
    ax = fig_pred.subplot(do_plot)
    Ymm = [0,max(Ym)]
    ax.plot(Ymm,Ymm,'g-')
    persons.plot( ax, Ym, Ypred )
    ax.set_title(title)
    ax.set_xlabel('IS, measured, mg/L')
    if eyl: ax.set_ylabel('IS, predicted, mg/L')
    
    ax = fig_ba.subplot(do_plot)
    mean_mp = (Ym+Ypred)/2.
    diff_mp = Ym-Ypred
    mm_mean_mp = [min(mean_mp),max(mean_mp)]
    md,s2 = mean(diff_mp), 2*diff_mp.std()
    #print mm_mean_mp,md,s2 #ax.clabel(contour,'AAA')#ax.set_xticklabels(['EE'],minor=True)
    def hline(l,txt):
        ax.axhline(y=l,ls=':',c='g')
        if txt: ax.annotate(txt,(mm_mean_mp[0],l),color='g')
    hline(md-s2,'Mean-2*SD')
    hline(md,'')
    hline(md+s2,'Mean+2*SD')
    persons.plot( ax, mean_mp, diff_mp )
    ax.set_title(title+', Bland-Altman')
    ax.set_xlabel('IS, (measured+predicted)/2, mg/L')
    if eyl: ax.set_ylabel('IS, (measured-predicted), mg/L')
    
    

fig_pred = SharingFigure()
fig_ba = SharingFigure()
inc('out26/','Univariate',221,0)
inc('out20/pca7','PCA, 7 components')
inc('out20/pca15','PCA, 15 components',222,1)
inc('out24/pls_9_','PLS, 9 components')
inc('out24/pls_14_','PLS, 14 components',223,0)
inc('out24/pls_pp_15_','PLS, pr., 15 components',224,1)
fig_pred.save('out29/4pred.png')
fig_ba.save('out29/4ba.png')

