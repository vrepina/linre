
from freq_pairs import load
from persons import Persons
(dis_list,res,exp_list) = load('linre_big.st')
persons = Persons(exp_list)

res.sort(key=lambda p:(p.ex,p.em))

class LinRModel:
    def get_y(m,x): return x * m.slope + m.intercept

from scipy.stats import linregress, spearmanr
for p in res:
    m = p.model = LinRModel()
    (m.slope,m.intercept,m.r_value,m.p_value,m.stderr) = linregress(p.flu,dis_list)
    p.corr_spearman = spearmanr(dis_list,p.flu)[0]

import matplotlib.pyplot as plt
for p in res:
    if abs(p.model.r_value) < 0.88 and p.corr_spearman < 0.883 : continue #984
    plt.figure()
    #plt.plot(p.flu,dis_list,'ro')
    persons.plot(plt,p.flu,dis_list)
    plt.plot(p.flu,[p.model.get_y(x) for x in p.flu],'g-')
    plt.title("ex: %d em: %d\ncorr: %f stderr: %f" % 
        (p.ex,p.em,p.model.r_value,p.model.stderr) )
    plt.xlabel('Fluorescence, nm')
    plt.ylabel('IS concentration, mg/L')
    plt.savefig("out4/%d-%d.png" % (p.ex,p.em))
    
#rgb cmyk w; o:

