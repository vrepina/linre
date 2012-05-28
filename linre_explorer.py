
from numpy import unique, empty, savez
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def freq3d_explore(ema,exa,data,pga,pg_indexer=0,mplot_inner=0,on_key_inner=0):
    """make grid for plotting"""
    uniq_exa, uidx_exa = unique(exa, return_inverse=True)
    uniq_ema, uidx_ema = unique(ema, return_inverse=True)
    xaa = empty((len(uniq_ema),len(uniq_exa)))
    yaa = empty((len(uniq_ema),len(uniq_exa)))
    zaaa = empty((len(uniq_ema),len(uniq_exa),len(pga)))
    xaa[uidx_ema,uidx_exa] = exa
    yaa[uidx_ema,uidx_exa] = ema
    zaaa[uidx_ema,uidx_exa] = data.T
    cur_sample = {'b':0,'g':0}
    def lplot(color):
        i = pg_indexer(cur_sample[color]) if pg_indexer else cur_sample[color]
        for j in range(xaa.shape[1]): 
            line = ax.plot(xaa[:,j],yaa[:,j],zaaa[:,j,i],color)
        return ( i, line, pga[i] )
    def mplot():
        bi, line_b, leg_b = lplot('b')
        gi, line_g, leg_g = lplot('g')
        if mplot_inner: mplot_inner(ax,gi)
        plt.legend( (line_b,line_g), (leg_b,leg_g) )
    def on_key(event):
        if event.key == ',': 
            cur_sample['b'] = cur_sample['b'] - 1
            cur_sample['g'] = cur_sample['g'] - 1
        elif event.key == '.': 
            cur_sample['b'] = cur_sample['b'] + 1
            cur_sample['g'] = cur_sample['g'] + 1
        elif event.key == '[': 
            cur_sample['g'] = cur_sample['g'] - 1
        elif event.key == ']': 
            cur_sample['g'] = cur_sample['g'] + 1
        if on_key_inner: on_key_inner(event.key)
        ax.cla()
        mplot()
        fig.canvas.draw()
    fig = plt.figure()
    ax = Axes3D(fig)
    fig.canvas.mpl_connect('key_press_event', on_key)
    plt.xlabel('EX, nm')
    plt.ylabel('EM, nm')
    mplot()
    plt.show()

def freq3d_save(fnpre,ema,exa,data,pga,zlabel=''):
    uniq_exa, uidx_exa = unique(exa, return_inverse=True)
    uniq_ema, uidx_ema = unique(ema, return_inverse=True)
    xaa = empty((len(uniq_exa),len(uniq_ema)))
    yaa = empty((len(uniq_exa),len(uniq_ema)))
    zaaa = empty((len(data),len(uniq_exa),len(uniq_ema)))
    xaa[uidx_exa,uidx_ema] = exa
    yaa[uidx_exa,uidx_ema] = ema
    for i in range(len(data)): zaaa[i,uidx_exa,uidx_ema] = data[i]
    savez(fnpre+'.3d.npz',
        titles=pga, xaa=xaa, yaa=yaa, zaaa=zaaa,
        xlabel='EX, nm', ylabel='EM, nm', zlabel=zlabel
    )
