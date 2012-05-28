
## extracting best eigen-vectors
from numpy import savez, load, array
best_cnt = 100
out_st = dict()
for k in ('0scatter','1cov','2corr'):
    in_st = load('out_big/linre8.'+k+'.out.npz')
    eva = in_st['eigval']
    eve = in_st['eigvec']
    ev_pairs = zip(eva,eve.T)
    ev_pairs.sort(reverse=1)
    ev_pairs_best = ev_pairs[0:best_cnt]
    eva_best = array([p[0] for p in ev_pairs_best])
    eve_best = array([p[1] for p in ev_pairs_best]).T
    out_st[k+'_eigval_best'] = eva_best
    out_st[k+'_eigvec_best'] = eve_best
    out_st[k+'_flu'] = in_st['flu']
savez('out_big/linre9.0.out.npz',**out_st)