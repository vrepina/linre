
from pyExcelerator import parse_xls
from pickle import Pickler
import re

exp_list = []
dis_list = []

def import_dis(filename,exp_colpos,dis_colpos):
    print 'opening y'
    sheet_cont = parse_xls(filename)[0][1];
    max_rowpos = 2
    for (rowpos,colpos) in sheet_cont:
        if max_rowpos < rowpos: max_rowpos = rowpos
    rowpos = 2
    while rowpos <= max_rowpos: 
        exp_pos = (rowpos,exp_colpos)
        dis_pos = (rowpos,dis_colpos)
        #if exp_pos in sheet_cont and dis_pos not in sheet_cont:
        #    print sheet_cont[exp_pos]
        if exp_pos in sheet_cont and dis_pos in sheet_cont:
            exp_list.append(sheet_cont[exp_pos])
            dis_list.append(sheet_cont[dis_pos])
            #print sheet_cont[exp_pos], sheet_cont[dis_pos]
        rowpos += 1
    #print len(exp_list), exp_list

import_dis(filename='linre_y.xls',exp_colpos=0,dis_colpos=13)
import_dis(filename='Link_HD_HDF_2008_27102010.xls',exp_colpos=8,dis_colpos=19)

num_finder = re.compile('^\d+')
data4hz = dict()
for sheet_name, values in parse_xls('linre_x_big.xls'):
    if sheet_name in exp_list:
        print sheet_name,' found'
        #if sheet_name=='F9' : print  values
        exp_index = exp_list.index(sheet_name)
        for rowpos, colpos in values:
            if rowpos>0 and colpos>0:
                ex = int(num_finder.match(values[(0,colpos)]).group())
                em = values[(rowpos,0)]
                hzkey = (ex,em)
                if hzkey not in data4hz: data4hz[hzkey] = [None] * len(exp_list)
                data4hz[hzkey][exp_index] = values[(rowpos,colpos)]
        print sheet_name,' parsed'

apicler = Pickler(open('linre_big.st','w'))
apicler.dump(dis_list)
apicler.dump(data4hz)
apicler.dump(exp_list)