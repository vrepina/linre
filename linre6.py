from freq_pairs import load
from scipy.linalg import lstsq 
from numpy import mat

(dis_list,res) = load('linre.st')
res.sort(key=lambda p:(p.ex,p.em))
in_mat = mat([p.flu for p in res]).T
out_mat = mat(dis_list).T
(x,residues,rank,s) = lstsq(in_mat,out_mat)

for (p,k) in zip(res,x): p.k = k
res.sort(key=lambda p:-abs(p.k))
for p in res[0:6]: print p.k, p.ex, p.em
    
"""
[ 0.00038485] 460 710
[ 0.00038418] 450 716
[ 0.00027918] 410 646
[ 0.00019384] 330 332
[ 0.0001862] 350 352
[ 0.00018589] 330 330
...
"""