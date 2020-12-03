#!/usr/bin/python
# coding: utf-8
import sys
from PyQt4 import QtGui
import numpy as np
import scipy.fftpack
import epics

# NEED TO INSTALL sudo yum install python-matplotlib-qt4
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class Main(QtGui.QDialog):

  def __init__(self, parent = None):
    super(Main, self).__init__(parent)
    self.bufferSize=1000
    self.scaleFactor=1 
    self.buffer=np.zeros(1000)
    self.bufferIndex=0
    self.dataPerSample=0;
    self.doFFTSkipCycles=0; 
    self.doFFTSkipCycleCounter=5; 
    self.pvname='IOC_SLIT:xr-PosAct'
    self.mypv = epics.PV(self.pvname)
    self.xlim=[0,2500]
    self.ylim=[0,5]
    self.firstPlot=1
    print self.mypv.get()
    print self.mypv.count, self.mypv.type
    print self.mypv.info
    self.initUI()

  def initUI(self):
    # set the layout
    self.setGeometry(100,100,800,500)
    self.setWindowTitle("FFT GUI")
    # a figure instance to plot on
    self.figure = Figure()
    self.canvas = FigureCanvas(self.figure)
    self.toolbar = NavigationToolbar(self.canvas, self)
    self.btnStart = QtGui.QPushButton('Start',self)
    self.btnStart.clicked.connect(self.calc)
    self.btnPaus = QtGui.QPushButton('Paus', self)     
    self.btnPaus.clicked.connect(self.paus)
    self.btnQuit = QtGui.QPushButton('Quit', self)     
    self.btnQuit.clicked.connect(self.quit)
    layout = QtGui.QVBoxLayout()
    layout.addWidget(self.toolbar)
    layout.addWidget(self.canvas)
    layout.addWidget(self.btnStart)
    layout.addWidget(self.btnPaus)
    layout.addWidget(self.btnQuit)
    self.setLayout(layout)

  def calc(self):    
    self.mypv.add_callback(self.onChanges)

  def paus(self):
    self.mypv.clear_callbacks()
    self.buffer.fill(0)    
    self.bufferIndex=0
 
  def onChanges(self,pvname=None, value=None, char_value=None, **kw):
    self.dataPerSample=1;
    if self.bufferIndex>=self.bufferSize:
      self.buffer.fill(0)
      self.bufferIndex=0
    self.buffer[self.bufferIndex:self.bufferIndex+self.dataPerSample]=value;
    self.bufferIndex=self.bufferIndex+self.dataPerSample
    if self.bufferIndex>=self.bufferSize:
      print "Buffer Full"
      self.doFFTSkipCycleCounter=self.doFFTSkipCycleCounter+1;
      if self.doFFTSkipCycleCounter>=self.doFFTSkipCycles:
        self.doFFTSkipCycleCounter=0
        self.doFFT(self.buffer)

  def doFFT(self,data):
    global bufferSize,buffer,bufferIndex,dataPerSample,doFFTSkipCycles,doFFTSkipCycleCounter
    # Number of samplepoints
    N = data.size
    # sample spacing
    T = 1.0 / (self.dataPerSample*1000)
    x = np.linspace(0.0, N*T, N)
    y = data*self.scaleFactor
    yf = scipy.fftpack.fft(y)
    xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
    yfft=2.0/N * np.abs(yf[:N//2]) # integer division
    ax = self.figure.add_subplot(111)
    self.xlim=ax.get_xlim()
    self.ylim=ax.get_ylim()
    ax.clear()
    ax.plot(xf,yfft, '*-')
    ax.grid()
    if not self.firstPlot:
      ax.set_xlim(self.xlim)
      ax.set_ylim(self.ylim)    

    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("Amplitude [g]")
    self.canvas.draw()
    self.firstPlot=0

  def quit(self):
    self.close()



