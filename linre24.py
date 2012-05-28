
"""
cross-validation of PLS model(s): plotting part

looking at residuals: samples with bad prediction m. b. have peaks on em=ex or too much peaks or to much data >60?

"""
#preprocess, plot_pred_only = '', 9
#preprocess, plot_pred_only = '', 14
preprocess, plot_pred_only = 'pp_', 15

from numpy import load, savez, arange, sqrt, mean
from numpy.linalg import norm
from sklearn.metrics import r2_score, mean_square_error
from linre_tools import AttrDict, RMSEP, BIAS, SE
from persons import Persons
import matplotlib.pyplot as plt


mds = AttrDict(load("out23/"+preprocess+"pred.npz"))
Y, Ypred4n, expa = mds.Y, mds.Ypred4n_components, mds.expa
n_components_list = arange(Ypred4n.shape[1])+1
def get_y_m_p(n_components): return (Y[:,0], Ypred4n[:,n_components-1])


title = 'PLS, K-Fold, '+str(len(Y))+' samples'

#"""
persons = Persons(mds.expa)
Ymm = [0,max(Y[:,0])]

def msavefig(fn):
    dfn = "out24/"+fn
    plt.savefig(dfn+".png")
    plt.savefig(dfn+".pdf")
    plt.savefig(dfn+".eps")
    plt.savefig(dfn+".svg")
    plt.cla()

def plot_pred(n_components):
    Ym, Ypred = get_y_m_p(n_components)
    ltitle = title+', '+str(n_components)+' components'
    fn = preprocess+"pred"+str(n_components)
    
    plt.plot(Ymm,Ymm,'g-')
    persons.plot( plt, Ym, Ypred )
    plt.title(ltitle)
    plt.xlabel('IS, measured, mg/L')
    plt.ylabel('IS, predicted, mg/L')
    msavefig(fn)
    
    plt.plot(Ymm,[0,0],'g-')
    persons.plot( plt, Ym, Ypred - Ym)
    plt.title(ltitle)
    plt.xlabel('IS, measured, mg/L')
    plt.ylabel('IS residuals (predicted-measured), mg/L')
    msavefig(fn+"resid")

    mean_mp = (Ym+Ypred)/2.
    diff_mp = Ym-Ypred
    mm_mean_mp = [min(mean_mp),max(mean_mp)]
    md,s2 = mean(diff_mp), 2*diff_mp.std()
    print mm_mean_mp,md,s2
    for l in [md-s2,md,md+s2]: plt.plot(mm_mean_mp,[l,l],'g-')
    persons.plot( plt, mean_mp, diff_mp )
    plt.title(ltitle+', Bland-Altman')
    plt.xlabel('IS, (measured+predicted)/2, mg/L')
    plt.ylabel('IS, (measured-predicted), mg/L')
    msavefig(fn+"ba")

if plot_pred_only: 
    plot_pred(plot_pred_only)
else:
    for n_components in n_components_list: plot_pred(n_components)

#"""

def apply_metrics(f): return [ f(*get_y_m_p(n)) for n in n_components_list ]

def plot_metrics(fn,t,m):
    plt.plot(n_components_list,m)
    plt.title(title)
    plt.xlabel('PC Count')
    plt.ylabel(t)
    msavefig(preprocess+fn)


plot_metrics('r2s','R2',apply_metrics(r2_score))
plot_metrics('mse','MSE',apply_metrics(mean_square_error))

# metrics.r2_score(y_true, y_pred) R^2 (coefficient of determination) regression score function

# metrics.mean_square_error(y_true, y_pred) Mean square error regression loss
# np.linalg.norm(y_pred - y_true) ** 2

plot_metrics('RMSEP','RMSEP, mg/L',apply_metrics(RMSEP))
print 'RMSEP', apply_metrics(RMSEP)

def TRVP(Ym,Ypred): return mean_square_error(Ym,Ypred) / len(Ym)

def correcting(m): return [ v+v*0.01*a for a,v in enumerate(m)]

plot_metrics('TRVP','TRVP',apply_metrics(TRVP))
plot_metrics('TRVP_c','TRVP, weighted',correcting(apply_metrics(TRVP)))

def EVRP(Ym,Ypred): return mean_square_error(Ym,Ypred) / norm(Ym)**2

plot_metrics('EVRP','ERVP',apply_metrics(EVRP))
plot_metrics('EVRP_c','ERVP, weighted',correcting(apply_metrics(EVRP)))

if plot_pred_only:
    Ym, Ypred = get_y_m_p(plot_pred_only)
    print 'RMSEP',  RMSEP(Ym, Ypred)
    print 'BIAS', BIAS(Ym, Ypred)
    print 'SE', SE(Ym, Ypred)
    savez('out24/pls_'+preprocess+str(plot_pred_only)+'_pred.npz',Ym=Ym,Ypred=Ypred,expa=expa)

"""
'',14
RMSEP 0.291831367524
BIAS 0.0112531154428
SE 0.29161432486
'',15
RMSEP 0.302189334688
BIAS 0.020807261928
SE{-1} 0.302546911485
SE 0.301472141085
'pp_',15
RMSEP 0.21918676345
BIAS -0.000475356595163
SE{-1} 0.219967663117
SE 0.21918624799

def RMSEP(Ym,Ypred): return norm(Ypred-Ym) / sqrt(len(Ym))
RMSEP = sqrt( power((disa_pred-disa),2).sum(axis=0) / len(disa) )


"""



