
from pyExcelerator import parse_xls
from pickle import Pickler
import re

sheet_cont = parse_xls('linre_y.xls')[0][1];
exp_colpos = 0
dis_colpos = 13
(exp_list,dis_list) = zip(*[
    ( sheet_cont[(i,exp_colpos)], sheet_cont[(i,dis_colpos)] )
    for i in range(2,11) 
    if (i,dis_colpos) in sheet_cont
])

num_finder = re.compile('^\d+')
data4hz = dict()
for sheet_name, values in parse_xls('linre_x.xls'):
    if sheet_name in exp_list:
        exp_index = exp_list.index(sheet_name)
        for rowpos, colpos in values:
            if rowpos>0 and colpos>0:
                ex = int(num_finder.match(values[(0,colpos)]).group())
                em = values[(rowpos,0)]
                hzkey = (ex,em)
                if hzkey not in data4hz: data4hz[hzkey] = [None] * len(exp_list)
                data4hz[hzkey][exp_index] = values[(rowpos,colpos)]

apicler = Pickler(open('linre.st','w'))
apicler.dump(dis_list)
apicler.dump(data4hz)
