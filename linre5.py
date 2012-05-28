from freq_pairs import load
from scipy.stats import pearsonr
from scipy.linalg import solve
from numpy import mat

(dis_list,res) = load('linre.st')

res.sort(key=lambda p:-abs(pearsonr(dis_list,p.flu)[0]))
res_best = res[:len(dis_list)]
res_best.sort(key=lambda p:(p.ex,p.em))

in_mat = mat([p.flu for p in res_best]).T
out_mat = mat(dis_list).T
k = solve(in_mat,out_mat) ## in_mat*k=out_mat
print k

"""
[[-1.41175523]
 [-2.14913538]
 [ 0.80070859]
 [ 1.28019631]
 [ 1.5132202 ]
 [-1.61472011]
 [-0.02564378]
 [ 1.74423183]]
"""