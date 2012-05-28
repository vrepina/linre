
"""
K-fold cross-validation of PCR model.
We want to find, how many components it would be better to have in our model.
Plots show RMSEP dependancy from number of components.

Our sample set is limited, so we decide to use cross validation.
In cross validation we only use the available training set objects, 
making models on parts of the data and testing on other parts. 
There is no independently drawn test set. 
Full cross validation or Leave-One-Out validation (LOO) means 
that we make as many sub-models as there are objects, 
every time leaving out just one of the objects and only use this for the testing.

We build multiple models that have different number of primary components and 
that are based on different calibration subsets of samples.
For leave-one-out method of cross validation number of models will be
up to thousands: max_components * number_of_samples.
Model building consists of two stages: PCA and MLR.
To optimize calculation time PCA stage can be cached 
for the same calibration subset and different number of components.
To make k-fold cross validation better reflect random reality conditions 
samples are shuffled before splitting into groups.

Question also is, what to do with outliers.
They need to be excluded from the fit sets.
But there are different samples in the reality, do we use them for test?
We can see, that including them makes plots fairly random and unusable.
Anyway we could implement 
the same automatic PCA pre-processing filter for outliers in production.
So we decide to exclude outliers from further exploration completely.
(test_by_good_only = 1)

We can vary group count from 2 to number of samples.
Resulting plots for less than 10 groups 
are random, unreliable and cannot be used.
For more than 10 groups up to LOO they become relatively similar.

Later we get additional samples from the lab.
Plots represents results for the initial and extended set (sample_set).
We can see that optimal number of components depends of fit set size.

Value of max_components is chosen so, 
that over this number plot behaviour is fairly predictable.

According to the plots for the initial sample set 
model groups with 4 and 14 components looks more interesting.
For extended sample set there may be 7 components.

"""
max_components = 45

from numpy import array, load, savez, arange, where, sqrt, power, empty, empty_like
from linre_tools import find_peaks, PCA
from scipy.linalg import lstsq 
from sklearn.cross_validation import KFold
from sklearn.utils import shuffle
import matplotlib.pyplot as plt

def pca_kfold(sample_set,test_by_good_only,kfold_group_count):
    l = load('linre_big'+sample_set+'.npz')
    flum = l['flum']
    disa = l['disa']
    exa = l['exa']
    expa = l['expa']

    X_orig = flum.T
    X_err, X_orig = find_peaks(X_orig,exa)

    X_orig, disa, expa = shuffle(X_orig, disa, expa, random_state=0)

    ## exclude outliers
    PC = PCA(n_components=2).fit_transform(X_orig.copy()) #mean inside
    PC1 = PC[:,0]
    good_std = PC1 < PC1.std()
    print expa[~good_std]
    if test_by_good_only:
        good_idxa, = where(good_std)
        good_std = good_std[good_idxa]
        X_orig = X_orig[good_idxa,:]
        disa = disa[good_idxa]
        expa = expa[good_idxa]

    def pca_calc(ia4fit):
        X4fit = X_orig[ia4fit,:]
        pca = PCA(n_components=max_components)
        PC = pca.fit_transform(X4fit.copy())
        return (pca,PC)

    cache = dict()
    def cached(f,l):
        k = tuple(l)
        if k not in cache: cache[k] = f(l)
        return cache[k]

    def make(n_components,ia4fit,ia4test):
        disa4fit = disa[ia4fit]
        X4test = X_orig[ia4test,:]
        (pca,PC) = cached(pca_calc,ia4fit)
        PC = PC[:,:n_components].copy()
        dis_mean = disa4fit.mean()
        (a,residues,rank,s) = lstsq(PC,disa4fit-dis_mean)
        PC = pca.transform(X4test.copy())[:,:n_components]
        return PC.dot(a[:,None])[:,0] + dis_mean #returns prediced dis

    x4plot, y4plot = [], []
    group_count = kfold_group_count(len(disa))
    disa_pred4n_components = empty((max_components,len(disa)))
    is_loo = group_count == len(disa)
    title_method = 'LOO' if is_loo else 'K-Fold '+str(group_count)+' groups'
    title_n = str(len(disa))+' samples'
    title_bad = '' if test_by_good_only else ' (inc. outliers)'
    for n_components in arange(max_components)+1:
        disa_pred = empty_like(disa)
        loo = KFold( n=len(disa), k=group_count, indices=False )
        for train, test in loo:
            ia4fit, = where( train & good_std )
            ia4test, = where( test )
            if len(ia4test): disa_pred[ia4test] = make(n_components,ia4fit,ia4test)
        disa_pred4n_components[n_components-1] = disa_pred
        RMSEP = sqrt( power((disa_pred-disa),2).sum(axis=0) / len(disa) )
        print n_components, RMSEP
        x4plot.append(n_components)
        y4plot.append(RMSEP)
    print 'plot start'
    plt.grid(True)
    plt.title(title_method+', '+title_n+title_bad)
    plt.xlabel('PC Count')
    plt.ylabel('RMSEP, mg/L')
    plt.plot(x4plot,y4plot)
    res_dir = "out18";
    res_name = "ts"+sample_set+"g"+str(test_by_good_only)+"k"+str(group_count);
    savez(res_dir+'/'+res_name+".npz",
        disa = disa,
        disa_pred4n_components = disa_pred4n_components,
        expa = expa
    )
    plt.savefig(res_dir+'/png/'+res_name+".png")
    plt.savefig(res_dir+'/pdf/'+res_name+".pdf")
    plt.cla()
    print 'plot finish'

#sample_set = '2'|''
#test_by_good_only = 1|0
#def kfold_group_count(n): return n|2|5|10|...
pca_kfold( sample_set='', test_by_good_only=0, kfold_group_count = lambda n:10 )
pca_kfold( sample_set='', test_by_good_only=1, kfold_group_count = lambda n:2 )
pca_kfold( sample_set='', test_by_good_only=1, kfold_group_count = lambda n:10 )
pca_kfold( sample_set='', test_by_good_only=1, kfold_group_count = lambda n:25 )
pca_kfold( sample_set='', test_by_good_only=1, kfold_group_count = lambda n:n )
pca_kfold( sample_set='2', test_by_good_only=1, kfold_group_count = lambda n:10 )
pca_kfold( sample_set='2', test_by_good_only=1, kfold_group_count = lambda n:n )

"""
Sample output:
1 0.638366149882
2 0.611018387347
3 0.535385808172
4 0.408440102746
5 0.433305556283
6 0.477242333262
7 0.652105017708
8 0.607428534576
9 0.406243626328
10 0.417936190597
11 1.21897283941
12 1.10295475783
13 0.628604703588
14 2.46010863345
15 2.23416094766
16 2.61514191362
17 2.7517276583
18 2.02400775108
19 1.50438749271
20 0.568894052659

1 0.606729289548
2 0.580431285985
3 0.520025973427
4 0.41007278086
5 0.418213704144
6 0.441054004871
7 0.409544804303
8 0.416424743658
9 0.40796953214
10 0.42370590916
11 0.39241618468
12 0.399737170537
13 0.387712085879
14 0.320996747827
15 0.324857530784
16 0.329413497272
17 0.329301680616
18 0.341266353622
19 0.345120279939
20 0.34892714452
"""

"""
PLS: Y=XB; B=W(P^TW)^{-1}Q^T
"""