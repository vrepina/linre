
from pickle import Unpickler

class FreqPair:
    pass

def load(fn):
    aunpickler = Unpickler(open(fn,'r'));
    dis_list = aunpickler.load()
    data4hz = aunpickler.load()
    exp_list = aunpickler.load()
    pairs = []
    for hzkey in data4hz:
        p = FreqPair()
        p.ex = hzkey[0]
        p.em = hzkey[1]
        p.flu = data4hz[hzkey]
        pairs.append(p)
    return (dis_list,pairs,exp_list)
