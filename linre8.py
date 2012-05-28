
## !! this may be not effective, use svd

##calculating eig
from freq_pairs import load
from numpy import savez, array, dot, mean, std

from scipy.linalg import eig

def calc_eig(fname,flu_mat):
    scatter_mat = dot(flu_mat.T,flu_mat);
    eigval, eigvec = eig(scatter_mat)
    savez( fname, flu=flu_mat, scatter=scatter_mat, eigval=eigval, eigvec=eigvec )

(dis_list,res,exp_list) = load('linre_big.st')
res.sort(key=lambda p:(p.ex,p.em))
flu_mat = array([p.flu for p in res]).T; #horiz

calc_eig('out_big/linre8.0scatter.out.npz',flu_mat)
flu_mat = flu_mat - mean(flu_mat,0)
calc_eig('out_big/linre8.1cov.out.npz',flu_mat)
flu_mat = flu_mat / std(flu_mat,0)
calc_eig('out_big/linre8.2corr.out.npz',flu_mat)

