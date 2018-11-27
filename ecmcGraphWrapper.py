#!/usr/bin/env python3.6
import sys
from PyQt5 import QtCore, QtWidgets
import numpy as np
import ecmcGraph as plt
from scipy.ndimage.interpolation import shift

ARRAY_BUFFER_SIZE=100
class ecmcGraphWrapper(QtWidgets.QDialog):

    def __init__(self, parent=None):
      super().__init__(parent=parent)
      self.windowReady=0
      self.graph=None
      self.xArr=np.arange(-ARRAY_BUFFER_SIZE+1,0+1)
      self.yArr=np.zeros(ARRAY_BUFFER_SIZE)
      self.valuesInBuffer=0
      
    def create_GUI(self):
      self.main_frame= QtWidgets.QFrame(self)
      self.main_layout = QtWidgets.QVBoxLayout()
      self.graph=plt.ecmcGraph(parent=self)
      self.setWindowTitle("ECMC: Graph")
      self.main_layout.addWidget(self.graph)
      self.main_frame.setLayout(self.main_layout)
      self.main_frame.resize(800,600) 
      self.graph.resize(800,600) 
      #self.graph.setXSize([-ARRAY_BUFFER_SIZE, 0])
      

      self.show()

    def openWindow(self):
        self.create_GUI()
      
    def setData(self,y):
      if self.graph is not None:
        
        #self.xArr=np.roll(self.xArr,-1)
        self.yArr=np.roll(self.yArr,-1)
        self.yArr[-1]=y
        self.valuesInBuffer=self.valuesInBuffer+1

        if self.valuesInBuffer<ARRAY_BUFFER_SIZE:
          #tmpX=self.xArr[-self.valuesInBuffer:-1]
          #tmpY=self.yArr[-self.valuesInBuffer:-1]
          #tmp=np.arange(self.valuesInBuffer-1)
          #print ("LEN X:" +str(len(tmpX)))
          #print ("LEN Y:" +str(len(tmp)))          
          self.graph.setData(self.xArr[-self.valuesInBuffer:-1],self.yArr[-self.valuesInBuffer:-1])
        else:  
        #  tmp=np.arange(self.valuesInBuffer-1)
        #  print ("LEN X:" +str(len(self.xArr)))
        #  print ("LEN Y:" +str(len(self.yArr)))          
          self.graph.setData(self.xArr,self.yArr)
        
        #print ("LEN X:" +str(len(self.xArr)))
        #print ("LEN Y:" +str(len(self.yArr)))
        #print ("X:" +str(self.xArr))
        #print ("Y:" +str(self.yArr))


