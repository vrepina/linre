
from numpy import array, savez, dtype
import freq_pairs

(dis_list,pairs,exp_list) = freq_pairs.load('linre_big.st')
pairs.sort(key=lambda p:(p.ex,p.em))
#savez('linre_big.npz0',dis_list=dis_list,pairs=pairs,exp_list=exp_list)
savez('linre_big2.npz',
    exa = array([p.ex for p in pairs]),
    ema = array([p.em for p in pairs]),
    flum = array([p.flu for p in pairs]), #X = flu.T
    disa = array(dis_list),               #Y = dis[:,None]
    expa = array(exp_list)
)