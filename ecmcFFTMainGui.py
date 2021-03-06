#*************************************************************************
# Copyright (c) 2020 European Spallation Source ERIC
# ecmc is distributed subject to a Software License Agreement found
# in file LICENSE that is included with this distribution. 
#
#   ecmcFFTMainGui.py
#
#  Created on: October 6, 2020
#      Author: Anders Sandström
#    
#  Plots two waveforms (x vs y) updates for each callback on the y-pv
#  
#*************************************************************************

import sys
import os
import epics
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.figure import Figure
from matplotlib.animation import TimedAnimation
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt 
import threading

# FFT object pvs <prefix>Plugin-FFT<fftPluginId>-<suffixname>
# IOC_TEST:Plugin-FFT0-stat# IOC_TEST:Plugin-FFT0-NFFT x
# IOC_TEST:Plugin-FFT0-Mode-RB x
# IOC_TEST:Plugin-FFT0-SampleRate-Act x
# IOC_TEST:Plugin-FFT0-Enable x
# IOC_TEST:Plugin-FFT0-Trigg x
# IOC_TEST:Plugin-FFT0-Source x
# IOC_TEST:Plugin-FFT0-Raw-Data-Act x
# IOC_TEST:Plugin-FFT0-PreProc-Data-Act 
# IOC_TEST:Plugin-FFT0-Spectrum-Amp-Act x
# IOC_TEST:Plugin-FFT0-Spectrum-X-Axis-Act x
# IOC_TEST:Plugin-FFT0-BuffIdAct
# IOC_TEST:Plugin-FFT0-Title

class comSignal(QObject):
    data_signal = pyqtSignal(object)

class ecmcFFTMainGui(QtWidgets.QDialog):
    def __init__(self,prefix=None,fftPluginId=None):        
        super(ecmcFFTMainGui, self).__init__()
        self.offline = False
        self.pvPrefixStr = prefix
        self.pvPrefixOrigStr = prefix  # save for restore after open datafile
        self.fftPluginId = fftPluginId
        self.fftPluginOrigId = fftPluginId
        self.allowSave = False
        self.path =  '.'
        self.unitRawY = "[]"
        self.unitSpectY = "[]"
        self.labelSpectY = "Amplitude"
        self.labelRawY = "Raw"
        self.title = ""
        self.NFFT = 1024
        self.sampleRate = 1000
        self.sampleRateValid = False
        self.FFTYDataValid = False
        self.FFTXDataValid = False
        self.RawYDataValid = False
        self.RawXDataValid = False
        if prefix is None or fftPluginId is None:
          self.offline = True
          self.pause = True
          self.enable = False           
        else:
          #Check for connection else go offline
          self.buildPvNames()
          pvtest  = epics.PV(self.pvNameSpectY)
          connected = pvtest.wait_for_connection(timeout=2)
          if connected:
            self.offline = False
            self.pause = False
          else: 
            self.offline = True
            self.pause = True
            self.enable = False
          pvtest.disconnect()

        # Callbacks through signals
        self.comSignalSpectX = comSignal()
        self.comSignalSpectX.data_signal.connect(self.callbackFuncSpectX)
        self.comSignalSpectY = comSignal()
        self.comSignalSpectY.data_signal.connect(self.callbackFuncSpectY)
        self.comSignalRawData = comSignal()
        self.comSignalRawData.data_signal.connect(self.callbackFuncrawData)
        self.comSignalEnable = comSignal()
        self.comSignalEnable.data_signal.connect(self.callbackFuncEnable)
        self.comSignalMode = comSignal()
        self.comSignalMode.data_signal.connect(self.callbackFuncMode)
        self.comSignalBuffIdAct = comSignal()
        self.comSignalBuffIdAct.data_signal.connect(self.callbackFuncBuffIdAct)
        self.startupDone=False
        
        self.pause = 0

        # Data
        self.spectX = None
        self.spectY = None
        self.rawdataY = None
        self.rawdataX = None
        self.enable = None

        self.pvMode = None

        self.createWidgets()
        self.connectPvs()
        self.setStatusOfWidgets()
        self.resize(1000,850)

        return

    def createWidgets(self):

        self.figure = plt.figure()
        self.plottedLineSpect = None
        self.plottedLineRaw = None
        self.axSpect = None
        self.axRaw = None
        self.canvas = FigureCanvas(self.figure)   
        self.toolbar = NavigationToolbar(self.canvas, self) 
        self.pauseBtn = QPushButton(text = 'pause')
        self.pauseBtn.setFixedSize(100, 50)
        self.pauseBtn.clicked.connect(self.pauseBtnAction)        
        self.pauseBtn.setStyleSheet("background-color: green")
        self.openBtn = QPushButton(text = 'open data')
        self.openBtn.setFixedSize(100, 50)
        self.openBtn.clicked.connect(self.openBtnAction)
        self.saveBtn = QPushButton(text = 'save data')
        self.saveBtn.setFixedSize(100, 50)
        self.saveBtn.clicked.connect(self.saveBtnAction)
        self.enableBtn = QPushButton(text = 'enable FFT')
        self.enableBtn.setFixedSize(100, 50)
        self.enableBtn.clicked.connect(self.enableBtnAction)
        self.triggBtn = QPushButton(text = 'trigg FFT')
        self.triggBtn.setFixedSize(100, 50)
        self.triggBtn.clicked.connect(self.triggBtnAction)
        self.zoomBtn = QPushButton(text = 'auto zoom')
        self.zoomBtn.setFixedSize(100, 50)
        self.zoomBtn.clicked.connect(self.zoomBtnAction)
        self.modeCombo = QComboBox()
        self.modeCombo.setFixedSize(100, 50)
        self.modeCombo.currentIndexChanged.connect(self.newModeIndexChanged)
        self.modeCombo.addItem("CONT")
        self.modeCombo.addItem("TRIGG")    
        self.progressBar = QProgressBar()
        self.progressBar.reset()
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100) #100%
        self.progressBar.setValue(0)
        self.progressBar.setFixedHeight(20)
    
        # Fix layout
        self.setGeometry(300, 300, 900, 700)
  
        layoutVert = QVBoxLayout()
        layoutVert.addWidget(self.toolbar) 
        layoutVert.addWidget(self.canvas) 

        layoutControl = QHBoxLayout() 
        layoutControl.addWidget(self.pauseBtn)
        layoutControl.addWidget(self.enableBtn)
        layoutControl.addWidget(self.triggBtn)
        layoutControl.addWidget(self.modeCombo)
        layoutControl.addWidget(self.zoomBtn)        
        layoutControl.addWidget(self.saveBtn)
        layoutControl.addWidget(self.openBtn)

        frameControl = QFrame(self)
        frameControl.setFixedHeight(70)
        frameControl.setLayout(layoutControl)


        layoutVert.addWidget(frameControl)
        layoutVert.addWidget(self.progressBar)
        self.setLayout(layoutVert)                

    def setStatusOfWidgets(self):
        self.saveBtn.setEnabled(self.allowSave)
        if self.offline:
            self.enableBtn.setStyleSheet("background-color: grey")
            self.enableBtn.setEnabled(False)
            self.pauseBtn.setStyleSheet("background-color: grey")
            self.pauseBtn.setEnabled(False)
            self.modeCombo.setEnabled(False)
            self.triggBtn.setEnabled(False)
            self.setWindowTitle("ecmc FFT Main plot: Offline")            
        else:
           self.modeCombo.setEnabled(True)
           # Check actual value of pvs
           enable = self.pvEnable.get()
           if enable is None:
             print("pvEnable.get() failed")
             return
           if(enable>0):
             self.enableBtn.setStyleSheet("background-color: green")
             self.enable = True
           else:
             self.enableBtn.setStyleSheet("background-color: red")
             self.enable = False
   
           self.sourceStr = self.pvSource.get(as_string=True)
           if self.sourceStr is None:
             print("pvSource.get() failed")
             return

           self.sampleRate = self.pvSampleRate.get()
           if self.sampleRate is None:              
              print("pvSampleRate.get() failed")
              return
           self.sampleRateValid = True

           self.NFFT = self.pvNFFT.get()        
           if self.NFFT is None:
             print("pvNFFT.get() failed")
             return

           self.mode = self.pvMode.get()    
           if self.mode is None:
             print("pvMode.get() failed")
             return

           self.modeStr = "NO_MODE"
           self.triggBtn.setEnabled(False) # Only enable if mode = TRIGG = 2
           if self.mode == 1:
               self.modeStr = "CONT"
               self.modeCombo.setCurrentIndex(self.mode-1) # Index starta t zero
   
           if self.mode == 2:
               self.modeStr = "TRIGG"
               self.triggBtn.setEnabled(True)
               self.modeCombo.setCurrentIndex(self.mode-1) # Index starta t zero
   
           self.setWindowTitle("ecmc FFT Main plot: prefix=" + self.pvPrefixStr + " , fftId=" + str(self.fftPluginId) + 
                               ", source="  + self.sourceStr + ", rate=" + str(self.sampleRate) + 
                               ", nfft=" + str(self.NFFT))       

    def buildPvNames(self):
           # Pv names based on structure:  <prefix>Plugin-FFT<fftPluginId>-<suffixname>
           self.pvNameSpectY = self.buildPvName('Spectrum-Amp-Act') # "IOC_TEST:Plugin-FFT1-Spectrum-Amp-Act"        
           self.pvNameSpectYDesc = self.buildPvName('Spectrum-Amp-Act.DESC') # "IOC_TEST:Plugin-FFT1-Spectrum-Amp-Act.DESC"
           self.pvNameSpectX = self.buildPvName('Spectrum-X-Axis-Act') # "IOC_TEST:Plugin-FFT1-Spectrum-X-Axis-Act"           
           self.pvNameRawDataY = self.buildPvName('Raw-Data-Act') # IOC_TEST:Plugin-FFT0-Raw-Data-Act
           self.pvNameRawDataYDesc = self.buildPvName('Raw-Data-Act.DESC') # IOC_TEST:Plugin-FFT0-Raw-Data-Act.DESC
           self.pvnNameEnable = self.buildPvName('Enable') # IOC_TEST:Plugin-FFT0-Enable
           self.pvnNameTrigg = self.buildPvName('Trigg') # IOC_TEST:Plugin-FFT0-Trigg
           self.pvnNameSource = self.buildPvName('Source') # IOC_TEST:Plugin-FFT0-Source
           self.pvnNameSampleRate = self.buildPvName('SampleRate-Act') # IOC_TEST:Plugin-FFT0-SampleRate-Act
           self.pvnNameNFFT = self.buildPvName('NFFT') # IOC_TEST:Plugin-FFT0-NFFT
           self.pvnNameMode = self.buildPvName('Mode-RB') # IOC_TEST:Plugin-FFT0-Mode-RB
           self.pvNameBuffIdAct = self.buildPvName('BuffIdAct')# IOC_TEST:Plugin-FFT0-BuffIdAct
           self.pvNameTitle = self.buildPvName('Title')# IOC_TEST:Plugin-FFT0-Title

    def buildPvName(self, suffixname):
        return self.pvPrefixStr + 'Plugin-FFT' + str(self.fftPluginId) + '-' + suffixname 

    def connectPvs(self):
        if self.offline:
            return

        if self.pvNameSpectX is None:
            raise RuntimeError("pvname X spect must not be 'None'")
        if len(self.pvNameSpectX)==0:
            raise RuntimeError("pvname  X spect must not be ''")

        if self.pvNameSpectY is None:
            raise RuntimeError("pvname y spect must not be 'None'")
        if len(self.pvNameSpectY)==0:
            raise RuntimeError("pvname  y spect must not be ''")

        if self.pvNameSpectYDesc is None:
            raise RuntimeError("pvname y spect desc must not be 'None'")
        if len(self.pvNameSpectYDesc)==0:
            raise RuntimeError("pvname  y spect desc must not be ''")

        if self.pvNameRawDataYDesc is None:
            raise RuntimeError("pvname y raw desc must not be 'None'")
        if len(self.pvNameRawDataYDesc)==0:
            raise RuntimeError("pvname  y raw desc must not be ''")

        if self.pvNameRawDataY is None:
            raise RuntimeError("pvname raw data must not be 'None'")
        if len(self.pvNameRawDataY)==0:
            raise RuntimeError("pvname raw data must not be ''")

        if self.pvnNameEnable is None:
            raise RuntimeError("pvname enable must not be 'None'")
        if len(self.pvnNameEnable)==0:
            raise RuntimeError("pvname enable must not be ''")

        if self.pvnNameTrigg is None:
            raise RuntimeError("pvname trigg must not be 'None'")
        if len(self.pvnNameTrigg)==0:
            raise RuntimeError("pvname trigg must not be ''")

        if self.pvnNameSource is None:
            raise RuntimeError("pvname source must not be 'None'")
        if len(self.pvnNameSource)==0:
            raise RuntimeError("pvname source must not be ''")

        if self.pvnNameSampleRate is None:
            raise RuntimeError("pvname sample rate must not be 'None'")
        if len(self.pvnNameSampleRate)==0:
            raise RuntimeError("pvname sample rate must not be ''")
        
        if self.pvnNameNFFT is None:
            raise RuntimeError("pvname NFFT must not be 'None'")
        if len(self.pvnNameNFFT)==0:
            raise RuntimeError("pvname NFFT must not be ''")
        
        if self.pvnNameMode is None:
            raise RuntimeError("pvname mode must not be 'None'")
        if len(self.pvnNameMode)==0:
            raise RuntimeError("pvname mode must not be ''")

        if self.pvNameBuffIdAct is None:
            raise RuntimeError("pvname buffactid must not be 'None'")
        if len(self.pvNameBuffIdAct)==0:
            raise RuntimeError("pvname buffactid must not be ''")

        if self.pvNameTitle is None:
            raise RuntimeError("pvname title must not be 'None'")
        if len(self.pvNameTitle)==0:
            raise RuntimeError("pvname title must not be ''")
                
        self.pvSpectX = epics.PV(self.pvNameSpectX)
        self.pvSpectY = epics.PV(self.pvNameSpectY)
        self.pvSpectYDesc = epics.PV(self.pvNameSpectYDesc)
        self.pvRawData = epics.PV(self.pvNameRawDataY)
        self.pvRawDataDesc = epics.PV(self.pvNameRawDataYDesc)
        self.pvEnable = epics.PV(self.pvnNameEnable)
        self.pvTrigg = epics.PV(self.pvnNameTrigg)
        self.pvSource = epics.PV(self.pvnNameSource)
        self.pvSampleRate = epics.PV(self.pvnNameSampleRate)
        self.pvNFFT = epics.PV(self.pvnNameNFFT)
        self.pvMode = epics.PV(self.pvnNameMode)
        self.pvBuffIdAct = epics.PV(self.pvNameBuffIdAct)
        self.pvTitle = epics.PV(self.pvNameTitle)
        self.pvSpectX.add_callback(self.onChangePvSpectX)
        self.pvSpectY.add_callback(self.onChangePvSpectY)
        self.pvRawData.add_callback(self.onChangePvrawData)
        self.pvEnable.add_callback(self.onChangePvEnable)
        self.pvMode.add_callback(self.onChangePvMode)
        self.pvBuffIdAct.add_callback(self.onChangePvBuffIdAct)
        
        if not self.pvRawData is None:
          self.unitRawY = '[' + self.pvRawData.units + ']'

        if not self.pvRawDataDesc is None:
          self.labelRawY = self.pvRawDataDesc.char_value
        else:
          self.labelRawY = pvNameRawDataY
          
        if not  self.pvSpectY is None:                  
          self.unitSpectY= '[' + self.pvSpectY.units + ']'
        
        if not self.pvSpectYDesc is None:
          self.labelSpectY = self.pvSpectYDesc.char_value
        else:
          self.labelSpectY = pvNameSpectY

        if not self.pvTitle is None:
          self.title = self.pvTitle.char_value
        else:
          self.title = "FFT"

        QCoreApplication.processEvents()
    
    ###### Pv monitor callbacks
    def onChangePvMode(self,pvname=None, value=None, char_value=None,timestamp=None, **kw):
        if self.pause: 
            return
        self.comSignalMode.data_signal.emit(value)

    def onChangePvEnable(self,pvname=None, value=None, char_value=None,timestamp=None, **kw):
        if self.pause: 
            return
        self.comSignalEnable.data_signal.emit(value)

    def onChangePvSpectX(self,pvname=None, value=None, char_value=None,timestamp=None, **kw):
        if self.pause: 
            return
        self.comSignalSpectX.data_signal.emit(value)

    def onChangePvSpectY(self,pvname=None, value=None, char_value=None,timestamp=None, **kw):
        if self.pause: 
            return
        self.comSignalSpectY.data_signal.emit(value)        

    def onChangePvrawData(self,pvname=None, value=None, char_value=None,timestamp=None, **kw):
        if self.pause: 
            return
        self.comSignalRawData.data_signal.emit(value)    

    def onChangePvBuffIdAct(self,pvname=None, value=None, char_value=None,timestamp=None, **kw):
        if self.pause: 
            return
        self.comSignalBuffIdAct.data_signal.emit(value)

    ###### Signal callbacks    
    def callbackFuncMode(self, value):
        if value < 1 or value> 2:
            self.modeStr = "NO_MODE"
            print('callbackFuncMode: Error Invalid mode.')
            return

        self.mode = value
        self.modeCombo.setCurrentIndex(self.mode-1) # Index starta t zero
        
        if self.mode == 1:
            self.modeStr = "CONT"
            self.triggBtn.setEnabled(False) # Only enable if mode = TRIGG = 2
                        
        if self.mode == 2:
           self.modeStr = "TRIGG"
           self.triggBtn.setEnabled(True)
                
        return

    def callbackFuncEnable(self, value):
        self.enable = value        
        if self.enable:
          self.enableBtn.setStyleSheet("background-color: green")
        else:
          self.enableBtn.setStyleSheet("background-color: red")
        return

    def callbackFuncSpectX(self, value):
        if(np.size(value)) > 0:
            self.spectX = value
            self.FFTXDataValid = True
        return

    def callbackFuncSpectY(self, value):
        if(np.size(value)) > 0:
            self.spectY = value
            self.FFTYDataValid = self.RawXDataValid
            self.plotAll()            
        return

    def callbackFuncrawData(self, value):
        if(np.size(value)) > 0:
            if (self.rawdataX is None or np.size(value) != np.size(self.rawdataY)) and self.sampleRateValid:
                self.rawdataX = np.arange(-np.size(value)/self.sampleRate, 0, 1/self.sampleRate)
                self.RawXDataValid = True
                
            self.rawdataY = value
            self.RawYDataValid = True
            self.plotAll()
        return

    def callbackFuncBuffIdAct(self, value):
        if self.NFFT is None:
          return
        if(self.NFFT>0):
          self.progressBar.setValue(value/self.NFFT*100)
          if value/self.NFFT*100 < 80 and value/self.NFFT*100 >1:
            self.FFTYDataValid = False
            self.RawYDataValid = False
        return

    ###### Widget callbacks
    def pauseBtnAction(self):   
        self.pause = not self.pause
        if self.pause:
            self.pauseBtn.setStyleSheet("background-color: red")
        else:
            self.pvPrefixStr = self.pvPrefixOrigStr  # Restore if dataset  was opened
            self.fftPluginId = self.fftPluginOrigId  # Restore if dataset  was opened
            self.buildPvNames()

            self.pauseBtn.setStyleSheet("background-color: green")
            # Retrigger plots with newest values
            self.comSignalSpectY.data_signal.emit(self.spectY)
            self.comSignalRawData.data_signal.emit(self.rawdataY)
        return

    def enableBtnAction(self):
        self.enable = not self.enable
        self.pvEnable.put(self.enable)
        if self.enable:
          self.enableBtn.setStyleSheet("background-color: green")
        else:
          self.enableBtn.setStyleSheet("background-color: red")
        return

    def triggBtnAction(self):
        self.pvTrigg.put(True)
        return

    def zoomBtnAction(self):
        
        if self.rawdataY is None:
            return
        if self.rawdataX is None:
            return
        if self.spectY is None:
            return
        if self.spectX is None:
            return
        if self.axSpect is None:
            return

        # Spect                
        self.axSpect.autoscale(enable=True)
        self.plotSpect(True)
        # rawdata
        self.plotRaw(True)

        return

    def newModeIndexChanged(self,index):
        if index==0 or index==1:
            if not self.offline and self.pvMode is not None:
               self.pvMode.put(index+1)
        return
    
    def openBtnAction(self):
        if not self.offline:
           self.pause = 1  # pause while open if online
           self.pauseBtn.setStyleSheet("background-color: red")
           QCoreApplication.processEvents()
                   
        fname = QFileDialog.getOpenFileName(self, 'Open file', self.path, "Data files (*.npz)")
        if fname is None:
            return
        if np.size(fname) != 2:            
            return
        if len(fname[0])<=0:
            return
        self.path = os.path.dirname(os.path.abspath(fname[0]))     
        
        npzfile = np.load(fname[0])

        # verify scope plugin
        if npzfile['plugin'] != "FFT":
            print ("Invalid data type (wrong plugin type)")
            return
        
        # File valid                 
        self.rawdataX     = npzfile['rawdataX']        
        self.rawdataY     = npzfile['rawdataY']        
        self.spectX       = npzfile['spectX']          
        self.spectY       = npzfile['spectY']          
        self.sourceStr    = str(npzfile['sourceStr'])
        self.sampleRate   = npzfile['sampleRate']      
        self.NFFT         = npzfile['NFFT']            
        self.mode         = npzfile['mode']            
        self.pvPrefixStr  = str(npzfile['pvPrefixStr'])
        self.fftPluginId  = npzfile['fftPluginId']
        if 'unitRawY' in npzfile:
          self.unitRawY = str(npzfile['unitRawY'])
        if 'unitSpectY' in npzfile:
          self.unitSpectY = str(npzfile['unitSpectY'])
        if 'labelRawY' in npzfile:
          self.labelRawY = str(npzfile['labelRawY'])
        if 'labelSpectY' in npzfile:
          self.labelSpectY = str(npzfile['labelSpectY'])                  
        if 'title' in npzfile:
          self.title = str(npzfile['title'])

        self.buildPvNames()
        
        # trigg draw
        self.FFTYDataValid = True
        self.FFTXDataValid = True
        self.RawYDataValid = True
        self.RawXDataValid = True
        self.sampleRateValid = True

        self.comSignalMode.data_signal.emit(self.mode)
        self.comSignalSpectX.data_signal.emit(self.spectX)
        self.comSignalSpectY.data_signal.emit(self.spectY)
        self.comSignalRawData.data_signal.emit(self.rawdataY)
        
        self.setStatusOfWidgets()

        self.startupDone=True
        self.zoomBtnAction()
        return

    def saveBtnAction(self):
        fname = QFileDialog.getSaveFileName(self, 'Save file', self.path, "Data files (*.npz)")
        if fname is None:
            return
        if np.size(fname) != 2:            
            return
        if len(fname[0])<=0:
            return
        # Save all relevant data
        np.savez(fname[0],
                 plugin                   = "FFT",
                 rawdataX                 = self.rawdataX,
                 rawdataY                 = self.rawdataY,
                 spectX                   = self.spectX,
                 spectY                   = self.spectY,     
                 sourceStr                = self.sourceStr,
                 sampleRate               = self.sampleRate,
                 NFFT                     = self.NFFT,
                 mode                     = self.mode,
                 pvPrefixStr              = self.pvPrefixStr,
                 fftPluginId              = self.fftPluginId,
                 unitRawY                 = self.unitRawY,
                 unitSpectY               = self.unitSpectY,
                 labelRawY                = self.labelRawY,
                 labelSpectY              = self.labelSpectY,
                 title                    = self.title
                 )

        self.path = os.path.dirname(os.path.abspath(fname[0]))

        return

    def plotAll(self):
        print("self.FFTYDataValid = " + str(self.FFTYDataValid))
        print("self.FFTXDataValid = " + str(self.FFTXDataValid))
        print("self.RawYDataValid = " + str(self.RawYDataValid))
        print("self.RawXDataValid   = " + str(self.RawXDataValid))
        
        if self.FFTYDataValid and self.FFTXDataValid and self.RawYDataValid and self.RawXDataValid:
          self.plotSpect()
          self.plotRaw()
          self.FFTYDataValid = False 
          self.RawYDataValid = False

    ###### Plotting
    def plotSpect(self, autozoom=False):
        if self.spectX is None:
            return
        if self.spectY is None:
            return
        
        # create an axis for spectrum
        if self.axSpect is None:
           self.axSpect = self.figure.add_subplot(212)

        # plot data 
        if self.plottedLineSpect is not None:
            self.plottedLineSpect.remove()

        self.plottedLineSpect, = self.axSpect.plot(self.spectX,self.spectY, 'b*-') 
        self.axSpect.grid(True)


        self.axSpect.set_xlabel("Frequency [Hz]")
        self.axSpect.set_ylabel(self.labelSpectY + ' ' +self.unitSpectY)        

        if autozoom:
           ymin = np.min(self.spectY)
           ymax = np.max(self.spectY)
           # ensure different values
           if ymin == ymax:
               ymin = ymin - 1
               ymax = ymax + 1   
           range = ymax - ymin
           ymax += range * 0.1
           ymin -= range * 0.1
           xmin = np.min(self.spectX)
           xmax = np.max(self.spectX)
           if xmin == xmax:
               xmin = xmin - 1
               xmax = xmax + 1
           range = xmax - xmin
           xmax += range * 0.02
           xmin -= range * 0.02
           self.axSpect.set_ylim(ymin,ymax)
           self.axSpect.set_xlim(xmin,xmax)

        # refresh canvas 
        self.canvas.draw()
        self.axSpect.autoscale(enable=False)

    def plotRaw(self, autozoom=False):
        if self.rawdataY is None:
            return

        if self.rawdataX is None:
            return

        # create an axis for spectrum
        if self.axRaw is None:
           self.axRaw = self.figure.add_subplot(211)


        # plot data 
        if self.plottedLineRaw is not None:
            self.plottedLineRaw.remove()

        self.plottedLineRaw, = self.axRaw.plot(self.rawdataX,self.rawdataY, 'b*-') 
        self.axRaw.grid(True)

        self.axRaw.set_xlabel('Time [s]')
        self.axRaw.set_ylabel(self.labelRawY + ' ' + self.unitRawY)
        self.axRaw.set_title(self.title)

        if autozoom:
           ymin = np.min(self.rawdataY)
           ymax = np.max(self.rawdataY)
           # ensure different values
           if ymin == ymax:
               ymin=ymin-1
               ymax=ymax+1
           range = ymax - ymin
           ymax += range * 0.1
           ymin -= range * 0.1
           xmin = np.min(self.rawdataX)
           xmax = np.max(self.rawdataX)
           if xmin == xmax:
               xmin = xmin - 1
               xmax = xmax + 1
           range = xmax - xmin
           xmax += range * 0.02
           xmin -= range * 0.02
           self.axRaw.set_ylim(ymin,ymax)
           self.axRaw.set_xlim(xmin,xmax)
    
        # refresh canvas 
        self.canvas.draw()
        self.allowSave = True
        self.saveBtn.setEnabled(True)
        self.axRaw.autoscale(enable=False)

def printOutHelp():
  print("ecmcFFTMainGui: Plots waveforms of FFT data (updates on Y data callback). ")
  print("python ecmcFFTMainGui.py <prefix> <fftId>")
  print("<prefix>:  Ioc prefix ('IOC_TEST:')")
  print("<fftId> :  Id of fft plugin ('0')")
  print("example : python ecmcFFTMainGui.py 'IOC_TEST:' '0'")
  print("Will connect to Pvs: <prefix>Plugin-FFT<fftId>-*")

if __name__ == "__main__":
    import sys    
    prefix = None
    fftid = None
    if len(sys.argv) == 1:
       prefix = None
       fftid = None
    elif len(sys.argv) == 3:
       prefix = sys.argv[1]
       fftid = int(sys.argv[2])
    else:
       printOutHelp()
       sys.exit()    
    app = QtWidgets.QApplication(sys.argv)
    window=ecmcFFTMainGui(prefix=prefix,fftPluginId=fftid)
    window.show()
    sys.exit(app.exec_())
