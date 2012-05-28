
"""
cross-validation of PLS model(s): fit/predict part
"""

from numpy import array, load, savez, arange, empty, empty_like
from sklearn.cross_validation import KFold
from sklearn.utils import shuffle
from sklearn.pls import PLSRegression
from linre_tools import AttrDict, find_peaks

def pls_kfold( sample_set, kfold_group_count, max_components, preprocess ):
    print "load...";
    l = AttrDict(load('linre_big'+sample_set+'.npz'))
    disa = l.disa
    expa = l.expa
    Y = disa[:,None]
    X = l.flum.T
    X, Y, expa = shuffle(X, Y, expa, random_state=1)
    print "fix...";
    X_err, X = find_peaks(X,l.exa)
    pls = PLSRegression( scale=False, algorithm='svd' )
    pls.fit(X=X,Y=Y)
    PC = pls.transform(X.copy())
    PC1 = PC[:,0]
    good = PC1 > -PC1.std()*2
    X, Y, expa = X[good,:], Y[good,:], expa[good]
    if preprocess:
        X[X<0.5]=0.5
        X = X**0.25
    #save?
    print "cross-validation...";
    group_count = kfold_group_count(len(disa))
    Ypred4n_components = empty((len(Y),max_components))
    for n_components in arange(max_components)+1:
        Ypred = empty_like(Y)
        loo = KFold( n=len(Y), k=group_count, indices=False )
        for fit, test in loo:
            pls = PLSRegression( 
                scale=False, 
                algorithm='svd', 
                n_components=n_components 
            )
            pls.fit( X=X[fit].copy(), Y=Y[fit].copy() )
            Ypred[test] = pls.predict(X[test].copy())
        Ypred4n_components[:,n_components-1] = Ypred[:,0]
        print "done for "+str(n_components)+" components"
    savez('out23/'+preprocess+'pred.npz',
        X=X, Y=Y, expa=expa, Ypred4n_components=Ypred4n_components
    )
pls_kfold( 
    sample_set='2', 
    kfold_group_count=lambda n:10, 
    max_components=40, 
    preprocess='pp_'
)