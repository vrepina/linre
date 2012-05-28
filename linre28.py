
"""
PLS searching for good preprocessing function;

A good way to improve our model may be to use more methods of data preprocessing.
This can help to get rid of noise and reveal linear dependencies.
We try different combination of functions then model and estimate result by RMSEP.
At first we look at the distribution of fluorescence values.
Most of fluorescence values are close to zero and many are in range from -0.4 to 0.
They seem to be random. We try to fix them: X[X<0.5]=0.5;
Then we try to make range of fluorescence values more uniform.
We tried normalizing samples and functions like log, power or exponent,
getting lower RMSEP.
The best result was seen with power (root): X = X**0.25, 
leading to RMSEP fall below 0.22 for model with 14 or more components.
Then we repeat some modelling steps and review scores/loading plots and metrics.
#goto linre21, 15 components;
At T1/T6 score plot samples A7-A9 stay aside.
#pic
A4-A6 was already excluded as an outliers and
that may mean hole A serie is different from others in some way.
#goto linre22;
At the loading plot we see more values at different frequences affect prediction result.
#pic
Also the one of the largest peaks is on the minimal excitation frequency.
This may mean having data for even smaller excitation frequency could improve the model.
#may be loadings become less smooth?
#goto linre23 then linre24
Prediction is improved comparing with the previous model.
#pic pred15.png vs pp_pred15.png
Though here N1 and N2 samples are worst predicted.
N1 is an edge sample, so it may be the reason.
But N2 is not, so those two may be somehow different from others.
RMSEP  0.219
BIAS  -4.75e-4
SE     0.220

"""

from numpy import load, empty_like, power, exp2
from sklearn.cross_validation import KFold
from sklearn.pls import PLSRegression
from linre_tools import AttrDict, RMSEP
import matplotlib.pyplot as plt

mds = AttrDict(load("out23/pred.npz"))
X, Y, expa = mds.X, mds.Y, mds.expa

X[X<0.5]=0.5 #0.7
X = X**0.25

group_count = 11
n_components_list = range(9,20)

for n_components in n_components_list:
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
    print n_components, RMSEP(Y[:,0],Ypred[:,0])

#n, bins, patches = plt.hist(X.flatten(),40,range=(0,2))
#plt.show()

"""
stuff:
print [v for v in X.flatten() if v<-0.4] #only 3 numbers from X <-0.4
X = (1-X)**2/X*2 #Kubelka-Munk function
"""
"""-
5 0.407984567727
6 0.354843551016
7 0.340217332243
8 0.328329231934
9 0.307778570868
10 0.312049887499
11 0.306605926147
12 0.30079621287
13 0.292756127605
14 0.291831367524
15 0.302189334688
16 0.323018154045
17 0.341347139689
18 0.344360376403
19 0.347
"""
"""
from sklearn.preprocessing import Normalizer
X = Normalizer().fit_transform(X)
5 0.368331701216
6 0.341066636364
7 0.314711665643
8 0.305805669789
9 0.306076920863
10 0.295166573581
11 0.290280585546
12 0.287890164885
13 0.298056530089
14 0.30116377397
15 0.316691569225
16 0.328264193624
17 0.340475215337
18 0.341717262079
19 0.35040160638
"""
""" X[X<1.]=0.; same 0.75
5 0.405245956416
6 0.349853892799
7 0.335586006229
8 0.321543415073
9 0.301810958542
10 0.304547672723
11 0.295804408511
12 0.284862658408
13 0.273373477495
14 0.271862884233 !!
15 0.281494063476
16 0.288579441748
17 0.296848585911
18 0.297130312628
19 0.309082086176
"""
""" <1=0 ==> Norm
5 0.366349506298
6 0.33936889903
7 0.311976589555
8 0.30173718267
9 0.300198276499
10 0.286382225404
11 0.280101224329
12 0.276150313739
13 0.283753559663
14 0.283123952214
15 0.288900227759
16 0.296775707159
17 0.304368067281
18 0.303252453648
19 0.30588747208
"""
""" <2.0=0
5 0.402678031234
6 0.346212083909
7 0.330180701801
8 0.309555669101
9 0.291772937144
10 0.295328390499
11 0.278079255841
12 0.265523278117
13 0.257855276824 !!
14 0.258029949865
15 0.259931720335
16 0.272207043121
17 0.275961953486
18 0.280099189006
19 0.283612437474
"""
""" <4.0=0
5 0.40066738941
6 0.337696636484
7 0.320912553168
8 0.311637895508
9 0.302092101654
10 0.295384888927
11 0.283638042836
12 0.277099583196
13 0.276940867191
14 0.2721800182
15 0.267844807372
16 0.273178833867
17 0.277109241502
18 0.27615193082
19 0.27482888414
20 0.2759968121
21 0.274553676191
22 0.2732247982
23 0.272418322149
24 0.272263551697
25 0.271854632529
26 0.271765797055
"""
"""
X[X<1.]=1.
X = np.log(X)
5 0.352494889662
6 0.319480782952
7 0.297734111849
8 0.289357359342
9 0.28509249549
10 0.250083315574
11 0.236851011686
12 0.242733897453
13 0.230600398009
14 0.223659246775
15 0.226325852278
16 0.223081757271
17 0.22062873162
18 0.223753521791
19 0.222463699889
20 0.220764583318
21 0.221919963439
22 0.223300604213
23 0.222606644369
24 0.223056089216
25 0.223126558708
26 0.223137535387
27 0.223120624972
28 0.22305195457
29 0.223045937935
"""
"""
X[X<0.5]=0.5
X = np.sqrt(X)
5 0.380150547684
6 0.324665645466
7 0.305693731174
8 0.284879374767
9 0.266629834013
10 0.257897859789
11 0.262300989921
12 0.245994634168
13 0.236748965451
14 0.224040766158
15 0.223214599791
16 0.222119475362
17 0.225138565064
18 0.222748868873
19 0.225218347382
"""
"""
X[X<0.5]=0.5
X = np.power(X,0.25)
5 0.355900886983
6 0.306042009959
7 0.284164040155
8 0.27702505192
9 0.264060382644
10 0.256456433711
11 0.251614237186
12 0.234957400767
13 0.224251971437
14 0.219930152365
15 0.21918676345     !!!!!!!
16 0.216847534689
17 0.218625781579
18 0.219170208183
19 0.218089450208
"""
"""
X[X<0.5]=0.5
X = np.exp2(any-X*0.5)
0.75 also good
5 0.370885569619
6 0.339537769051
7 0.290318632238
8 0.287483049359
9 0.264621156962
10 0.238276583752
11 0.23808673378
12 0.228696927435
13 0.22249570783
14 0.218338113194
15 0.22143933551
16 0.223181218677
17 0.223214728596
18 0.223114669828
"""
