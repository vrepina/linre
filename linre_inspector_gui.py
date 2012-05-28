#!/usr/bin/python

import sys
import os
from numpy import load
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from linre_tools import AttrDict

def main():
    color2item = dict()
    def add_slides(idx,slide_list,color):
        slide_list.clear()
        path = fs_model.filePath(idx)
        if not os.path.isfile(path): return
        l = AttrDict(load(str(path)))
        titles, xaa, yaa, zaaa = l.titles, l.xaa, l.yaa, l.zaaa
        ax.set_xlabel(l.xlabel)
        ax.set_ylabel(l.ylabel)
        ax.set_zlabel(l.zlabel)
        for i,title in enumerate(titles):
            QtGui.QListWidgetItem(title,slide_list).data4plot = \
                AttrDict(dict(xaa=xaa,yaa=yaa,zaa=zaaa[i],color=color,title=title))
    def replot():
        ax.clear()
        ax.mouse_init()
        lines, legends = [], []
        for lcolor, it in color2item.iteritems():
            for j in range(len(it.xaa)): 
                line = ax.plot(it.xaa[j],it.yaa[j],it.zaa[j],it.color)
            if line:
                lines.append(line)
                legends.append(it.title)
        if lines: ax.legend( lines, legends )
        canvas.draw()
    def setup_slide_selector(rn,color):
        fs_tree_view = QtGui.QTreeView()
        fs_tree_view.setModel(fs_model)
        fs_tree_view.setRootIndex(fs_model.index(fs_model.rootPath()));
        slide_list = QtGui.QListWidget()
        def fs_activated(i): add_slides(i,slide_list,color)
        fs_tree_view.activated.connect(fs_activated)
        def slide_changed(item,prev_item):
            if item: color2item[color] = item.data4plot
            else: del color2item[color]
            replot()
        slide_list.currentItemChanged.connect(slide_changed)
        lt_grid.addWidget(fs_tree_view,rn,0)
        lt_grid.addWidget(slide_list,rn,1)

    app = QtGui.QApplication(sys.argv)
    splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
    splitter.setHandleWidth(20)

    lt_panel = QtGui.QWidget(splitter)
    rt_panel = QtGui.QWidget(splitter)
    
    fs_model = QtGui.QFileSystemModel()
    pwd = QtCore.QDir.currentPath()
    fs_model.setNameFilterDisables(False)
    fs_model.setNameFilters(['*.3d.npz'])
    fs_model.setRootPath(pwd) #for tracking only
    
    lt_grid = QtGui.QGridLayout(lt_panel)
    
    setup_slide_selector(0,'g')
    setup_slide_selector(1,'b')

    vbox = QtGui.QVBoxLayout()
    rt_panel.setLayout(vbox)
    
    fig = Figure((6.0, 4.0), dpi=100)
    canvas = FigureCanvas(fig)
    vbox.addWidget(canvas)
    ax = Axes3D(fig)
    
    mpl_toolbar = NavigationToolbar(canvas,rt_panel)
    vbox.addWidget(mpl_toolbar)
    
    splitter.show()
    sys.exit(app.exec_())


if __name__ == '__main__': main()
