
from numpy import hstack, mean, where, repeat

def mshift(X,dir):
    """shift 2d array: +left -right"""
    return hstack((X[:,dir:],X[:,:dir]))
def find_peaks(X,exa):
    """calculate array of mean values of X with shape of X;
    mean of 2 next values, or just 1 next value at the edge;
    edge is determined by exm, where its different from the next cell;
    """
    exm = exa[None,:]
    e = repeat(exm,X.shape[0],0)
    lt_edge, rt_edge = e != mshift(e,-1), e != mshift(e,1)
    X_shrt, X_shlt = mshift(X,-1), mshift(X,1)
    a_next_mean = mean((X_shrt,X_shlt),0)
    next_mean = where(lt_edge,X_shlt,where(rt_edge,X_shrt,a_next_mean))
    err2d = abs(X-next_mean) > 50
    removed = where( err2d , next_mean, X )
    return(err2d,removed)
    
################################################################################
class AttrDict(dict):
    """allows to access dict['item'] as obj.attr
    """
    def __getattr__(self, attr): return self[attr]
    def __setattr__(self, attr, value): self[attr] = value
def fret(loc): 
    """return fret(locals()) -- returns filtered dict of locals
    """
    d = AttrDict()
    for i in loc: 
        if 'ret_'+i in loc and loc['ret_'+i]: d[i] = loc[i]
    return d

################################################################################
## uses find_peaks, fret
import sys
#sys.path.append("/home/rewlad/vktc/scikit-learn") 
from sklearn.decomposition import PCA
from numpy import where, arange

def take_good(orig,pco): return orig.take(pco.good_idxa,axis=0)

def pcs_calc(
    exa, flum, max_components, no_peaks, normalize, recalc_wo_outliers,
    ret_X=0, ret_PC=0, ret_PC_std=0, ret_good_idxa=0, ret_pca=0, ret_loadings=0
):
    def calc(X_in):
        X = X_in - X_in.mean(axis=0) ## not -=
        if normalize: X /= X.std(axis=0)
        pca = PCA(n_components=max_components)
        return X, pca, pca.fit_transform(X)
    X_orig = flum.T.copy()
    if no_peaks: X_err, X_orig = find_peaks(X_orig,exa)
    X, pca, PC = calc(X_orig)
    PC1 = PC[:,0]
    PC_std = PC.std(axis=0) 
    good_idxa = arange(len(PC1))
    if recalc_wo_outliers:
        good_idxa, = where( PC1<PC_std[0] ) #std is just random border
        X, pca, PC = calc(X_orig.take(good_idxa,axis=0))
    loadings = pca.components_;
    return fret(locals())

################################################################################
from numpy import sqrt, mean
from numpy.linalg import norm
def RMSEP(Ym,Ypred): return norm(Ypred-Ym) / sqrt(len(Ym))
def BIAS(Ym,Ypred): return mean(Ym-Ypred)
def SE(Ym,Ypred): 
    e = Ym-Ypred
    return sqrt( ((e-BIAS(Ym,Ypred))**2).sum(axis=0) / (len(e)) ) #len-1?
