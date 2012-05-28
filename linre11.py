
from numpy import load, dot, array
from numpy.linalg import lstsq
import freq_pairs
from persons import Persons

(dis_list,res,exp_list) = freq_pairs.load('linre_big.st')
dis = array(dis_list)
persons = Persons(exp_list)

in_st = load('out_big/linre9.0.out.npz')
k = '0scatter'
eve = in_st[k+'_eigvec_best']
flu = in_st[k+'_flu']

eva_cnt = 10#len(dis) #10
eve = eve[:,:eva_cnt]
pcv = dot(flu,eve) #primary component values


lstsq_res = lstsq(pcv,dis)
a = lstsq_res[0]
#print eve.shape, flu.shape, pcv, lstsq_res[0]
mdis = dot(pcv,a[:,None])[:,0] #[:,None] turns 1D array to vertical 2D
#print mdis
import matplotlib.pyplot as plt
plt.figure()
plt.plot([0,max(dis)],[0,max(dis)],'g-')
persons.plot(plt,dis,mdis)
plt.show()