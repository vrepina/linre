
"""
draft

"""
sample_set = '2' #'2'|''
max_components = 45
test_by_good_only = 1; #True|False
def kfold_group_count(n): return 10 #n|2|5

from numpy import array, load, arange, where, sqrt, power, empty_like
from linre_tools import find_peaks, PCA
from scipy.linalg import lstsq 
from sklearn.cross_validation import KFold
from sklearn.utils import shuffle
import matplotlib.pyplot as plt

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
for n_components in [15]:
    disa_pred = empty_like(disa)
    loo = KFold( n=len(disa), k=group_count, indices=False )
    for train, test in loo:
        ia4fit, = where( train & good_std )
        ia4test, = where( test )
        if len(ia4test): disa_pred[ia4test] = make(n_components,ia4fit,ia4test)
    RMSEP = sqrt( power((disa_pred-disa),2).sum(axis=0) / len(disa) )
    BIAS = (disa-disa_pred).sum(axis=0) / len(disa) 
    e=disa-disa_pred
    SE = sqrt( power((e-BIAS),2).sum(axis=0) / (len(disa)-1) )
    print BIAS, SE
        
        
    plt.grid(True)
    plt.title('plotting predicted vs measured')
    plt.xlabel('Measured')
    plt.ylabel('Predicted')
    plt.plot(disa,disa_pred, 'ro')
    plt.plot([0,3],[0,3])
    plt.savefig("out19/%d.png" % (n_components))   
"""    
    print n_components, RMSEP
    x4plot.append(n_components)
    y4plot.append(RMSEP)

plt.grid(True)
plt.title('K-Fold')
plt.xlabel('PC Count')
plt.ylabel('RMSEP')
plt.plot(x4plot,y4plot)
#plt.show()

res_dir = "out18";
res_name = "s"+sample_set+"g"+str(test_by_good_only)+"k"+str(group_count);
plt.savefig(res_dir+'/'+res_name+".png")
plt.savefig(res_dir+'/pdf/'+res_name+".pdf")
"""
# ?? In cross validation we only use the available training set objects, 
# making models on parts of the data and testing on other parts. 
# There is no independently drawn test set. 
# Full cross validation or Leave-One-Out validation (LOO) means 
# that we make as many sub-models as there are objects, 
# every time leaving out just one of the objects and only use this for the testing.


