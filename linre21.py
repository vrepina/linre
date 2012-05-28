
"""
PLS probe, scores
"""

sample_set = '2'
samples_in_testing_set = 40
n_components = 15
preprocess = 'pp_' #|''

from numpy import array, load, savez, where, arange, logical_not, hstack
from numpy.linalg import inv
from sklearn.utils import shuffle
from sklearn.pls import PLSRegression
import matplotlib.pyplot as plt
from linre_tools import find_peaks
from persons import Persons

out_pre = "out21/"+preprocess

def plot_scores(fn,expa,x,y,xl,yl,title=''):
    Persons(expa).plot(plt,x,y)
    plt.title('PLS, '+str(len(y))+' samples'+title)
    plt.xlabel(xl)
    plt.ylabel(yl)
    plt.savefig(out_pre+"scores"+fn+".png")
    plt.cla()

print "load..."
l = load('linre_big'+sample_set+'.npz')
flum = l['flum']
disa = l['disa']
exa = l['exa']
expa = l['expa']

Y = disa[:,None]
X = flum.T

X, Y, expa = shuffle(X, Y, expa, random_state=1)

print "fix peaks..."

X_err, X = find_peaks(X,exa)

print "fix outliers..."

pls = PLSRegression( scale=False, algorithm='svd' )
pls.fit(X=X,Y=Y)
PC = pls.transform(X.copy())
PC1, PC2 = PC[:,0], PC[:,1]
good = PC1 > -PC1.std()*2
plot_scores(fn='_bad_1', expa=expa, x=PC1,y=PC2, xl='T1',yl='T2', title=', bad')
print expa[logical_not(good)]
X, Y, expa = X[good,:], Y[good,:], expa[good]

print "preprocess with power..."

if preprocess:
    X[X<0.5]=0.5
    X = X**0.25

print "fit..."
a4fit = arange(len(X)) >= samples_in_testing_set
a4test = logical_not(a4fit)
X4fit,  Y4fit,  expa4fit  = X[a4fit ,:], Y[a4fit ,:], expa[a4fit ]
X4test, Y4test, expa4test = X[a4test,:], Y[a4test,:], expa[a4test]

pls = PLSRegression(n_components=n_components,algorithm='svd',scale=False)
pls.fit(X=X4fit,Y=Y4fit)

print "predict..."

Y_pred = pls.predict(X4test.copy())

dis4test = Y4test[:,0]
dis_pred = Y_pred[:,0]
dis_max = max(disa)
#dis_pred = where(dis_pred<dis_max+1,where(dis_pred<-1,-1,dis_pred),dis_max+1)

persons = Persons(expa4test)

#print ia4test, ia4fit, logical_not(a4fit & good_std)
#print expa4test.shape, dis4test.shape, dis_pred.shape, Y.shape, Y4test.shape, Y_pred.shape

plt.plot([0,dis_max],[0,dis_max],'g-')
persons.plot(plt,dis4test,dis_pred)
plt.savefig(out_pre+"pred.png")
plt.cla()

print "fit..."

pls = PLSRegression(n_components=n_components,algorithm='svd',scale=False)
pls.fit(X=X,Y=Y)

print "save..."
"""
print pls.x_loadings_.shape, pls.x_weights_.shape, pls.x_rotations_.shape, \
      pls.y_loadings_.shape
"""
savez(out_pre+"loadings.npz",
    x_loadings = pls.x_loadings_,
    x_weights  = pls.x_weights_,
    x_rotations = pls.x_rotations_,
    y_loadings = pls.y_loadings_,
    coefs = pls.coefs,
    x_mean = pls.x_mean_,
    y_mean = pls.y_mean_
)
print "scores..."
x_scores, y_scores = pls.transform( X = X.copy(), Y = Y.copy() )

for c in range(1,n_components):
    px, py = x_scores[:,0], x_scores[:,c]
    xl, yl = 'T1', 'T'+str(c+1)
    plot_scores( fn='_ok_x_'+str(c), expa=expa, x=px, y=py, xl=xl, yl=yl )
    
"""y scores is just like y"""
plot_scores(fn='_ok_y',expa=expa,x=Y[:,0],y=y_scores,xl='',yl='')

for c in range(0,n_components):
    px, py = y_scores, x_scores[:,c]
    xl, yl = 'U1', 'T'+str(c+1)
    plot_scores( fn='_ok_yx_'+str(c), expa=expa, x=px, y=py, xl=xl, yl=yl )


