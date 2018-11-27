#!/usr/bin/env python3.6

from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
import numpy as np


class ecmcGraph(pg.GraphicsWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        pg.setConfigOptions(antialias=False) # True seems to work as well
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.plotItem = self.addPlot(title="")        
        self.plotItem.setDownsampling(mode='peak')
        self.plotItem.setClipToView(True)
        self.plotDataItem = self.plotItem.plot([], pen=None,symbolBrush=(255,0,0), symbolSize=5, symbolPen=None)
        
        #self.plotDataItem = self.plotItem.plot([], pen=None)

    def setData(self, x, y):
        self.plotDataItem.setData(y)        

    def setXSize(self, xSize):
      self.plotItem.setRange(xRange=xSize)

def main():
    app = QtWidgets.QApplication([])
    pg.setConfigOptions(antialias=False) # True seems to work as well
    win = ecmcGraph()
    win.show()
    win.resize(800,600) 
    win.raise_()
    app.exec_()

if __name__ == "__main__":
    main()
