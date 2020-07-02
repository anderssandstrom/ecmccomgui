###################################################################
#                                                                 #
#                    PLOT A LIVE GRAPH (PyQt5)                    #
#                  -----------------------------                  #
#            EMBED A MATPLOTLIB ANIMATION INSIDE YOUR             #
#            OWN GUI!                                             #
#                                                                 #
###################################################################

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets

from PyQt5.QtCore import *
from PyQt5.QtGui import *
import functools
import numpy as np
import random as rd
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.figure import Figure
from matplotlib.animation import TimedAnimation
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import time
import threading

# ADD buffer size
# Auto zoom button
# make clear button work
# Y low and high working

class ecmcTrend(QtWidgets.QDialog):
    def __init__(self):
        super(ecmcTrend, self).__init__()
        # Define the geometry of the main window
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("ECMC: Plot")
        # Create FRAME_A
        self.FRAME_A = QFrame(self)
        self.FRAME_A.setStyleSheet("QWidget { background-color: %s }" % QColor(210,210,235,255).name())
        self.LAYOUT_A = QGridLayout()
        self.FRAME_A.setLayout(self.LAYOUT_A)
        # self.setCentralWidget(self.FRAME_A)
        # Place the zoom button
        self.lineEditZoomHigh = QLineEdit(text = '100')
        self.lineEditZoomHigh.setFixedSize(100, 50)
        #self.lineEditZoomHigh.returnPressed.connect(self.lineEditHighAction)

        self.lineEditZoomLow = QLineEdit(text = '-100')
        self.lineEditZoomLow.setFixedSize(100, 50)
        #self.lineEditZoomLow.returnPressed.connect(self.lineEditLowAction)

        self.zoomBtn = QPushButton(text = 'zoom auto')
        self.zoomBtn.setFixedSize(100, 50)
        self.zoomBtn.clicked.connect(self.zoomBtnAction)

        #self.clearBtn = QPushButton(text = 'clear')
        #self.clearBtn.setFixedSize(100, 50)
        #self.clearBtn.clicked.connect(self.clearBtnAction)

        self.pauseBtn = QPushButton(text = 'pause')
        self.pauseBtn.setFixedSize(100, 50)
        self.pauseBtn.clicked.connect(self.pauseBtnAction)

        self.zoomLowBtn = QPushButton(text = '>')
        self.zoomLowBtn.setFixedSize(100, 50)
        self.zoomLowBtn.clicked.connect(self.zoomLowBtnAction)

        self.zoomHighBtn = QPushButton(text = '>')
        self.zoomHighBtn.setFixedSize(100, 50)
        self.zoomHighBtn.clicked.connect(self.zoomHighBtnAction)
        
        self.spacerUpper = QSpacerItem(100,10)
        self.spacerLower = QSpacerItem(100,10)
        

        self.LAYOUT_A.addWidget(self.lineEditZoomHigh, *(0,0))
        self.LAYOUT_A.addWidget(self.zoomHighBtn, *(1,0))
        self.LAYOUT_A.addItem(self.spacerUpper, *(2,0))
        self.LAYOUT_A.addWidget(self.zoomBtn, *(3,0))
        #self.LAYOUT_A.addWidget(self.clearBtn, *(4,0))
        self.LAYOUT_A.addWidget(self.pauseBtn, *(4,0))
        self.LAYOUT_A.addItem(self.spacerLower, *(5,0))
        self.LAYOUT_A.addWidget(self.zoomLowBtn, *(6,0))
        self.LAYOUT_A.addWidget(self.lineEditZoomLow, *(7,0))

        # Place the matplotlib figure
        self.myFig = CustomFigCanvas()
        self.myFig.setFixedSize(500,300 )
        self.toolbar = NavigationToolbar(self.myFig, self)
        self.LAYOUT_A.addWidget(self.toolbar, *(0,1))
        self.LAYOUT_A.addWidget(self.myFig, *(1,1))
        self.lineEditZoomLow.setText(str(self.myFig.getYLims()[0]))
        self.lineEditZoomHigh.setText(str(self.myFig.getYLims()[1]))
        
        return

    def zoomBtnAction(self):        
        self.myFig.zoomAuto()
        self.lineEditZoomLow.setText(str(np.round(self.myFig.getYLims()[0]*100)/100))
        self.lineEditZoomHigh.setText(str(np.round(self.myFig.getYLims()[1]*100)/100))
        return

    def zoomHighBtnAction(self):
        value = float(self.lineEditZoomHigh.text())
        self.myFig.zoomHigh(value)
        return

    def zoomLowBtnAction(self):
        value = float(self.lineEditZoomLow.text())
        self.myFig.zoomLow(value)
        return

    #def clearBtnAction(self):
    #    print("clear")
    #    self.myFig.clearData()
    #    return

    def pauseBtnAction(self):        
        self.myFig.pauseUpdate()
        return

    def lineEditHighAction(self):
        print("lineEditHighAction")
        value = float(self.lineEditZoomHigh.text())
        self.myFig.zoomHigh(value)
        #self.myFig.pauseUpdate()
        return

    def lineEditLowAction(self):
        print("lineEditLowAction")
        value = float(self.lineEditZoomLow.text())
        self.myFig.zoomLow(value)
        #self.myFig.pauseUpdate()
        return

    def addData_callbackFunc(self, value):
        self.myFig.addData(value)
        return

''' End Class '''


class CustomFigCanvas(FigureCanvas, TimedAnimation):
    def __init__(self):
        self.pause = 0
        self.addedData = []
        self.exceptCount = 0
        self.autoZoom =  False
        print(matplotlib.__version__)
        # The data
        self.xlim = 1000
        self.n = np.linspace(0, self.xlim - 1, self.xlim)
        self.y = (self.n * 0.0)
        # The window
        self.fig = Figure(figsize=(5,5), dpi=100)
        self.ax1 = self.fig.add_subplot(111)        
        # self.ax1 settings
        self.ax1.set_xlabel('time')
        self.ax1.set_ylabel('data')
        self.line1 = Line2D([], [], color='blue')
        self.line1_tail = Line2D([], [], color='red', linewidth=2)
        self.line1_head = Line2D([], [], color='red', marker='o', markeredgecolor='r')
        self.ax1.add_line(self.line1)
        self.ax1.add_line(self.line1_tail)
        self.ax1.add_line(self.line1_head)
        self.ax1.set_xlim(0, self.xlim - 1)
        self.ax1.set_ylim(-100, 100)
        self.ax1.grid()
        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval = 50, blit = True)
        return

    def new_frame_seq(self):
        return iter(range(self.n.size))

    #def clearData(self):
    #    print("clearData")
    #    self.ax1.remove()

    def pauseUpdate(self):
        print("pause")        
        if self.pause:
          self.pause = 0
        else:
          self.pause = 1

    def _init_draw(self):
        lines = [self.line1, self.line1_tail, self.line1_head]
        for l in lines:
            l.set_data([], [])
        return

    def addData(self, value):         
        if self.pause == 0:
          self.addedData.append(value)
        return

    def zoomAuto(self):
        bottom = np.min(self.y)
        top = np.max(self.y)
        range = top - bottom
        top += range * 0.1
        bottom -= range *0.1
        self.ax1.set_ylim(bottom,top)
        self.draw()
        return
    
    def zoomLow(self, value):
        top = self.ax1.get_ylim()[1]
        bottom = value
        print('Top: ' + str(top) +', Bottom: ' + str(bottom)+ ', ylim: ' + str(self.ax1.get_ylim()))
        self.ax1.set_ylim(bottom,top)
        self.draw()
        return

    def zoomHigh(self, value):
        bottom = self.ax1.get_ylim()[0]
        top = value
        print('Top: ' + str(top) +', Bottom: ' + str(bottom))
        self.ax1.set_ylim(bottom,top)
        self.draw()
        return

    def _step(self, *args):
        # Extends the _step() method for the TimedAnimation class.
        try:
            TimedAnimation._step(self, *args)
        except Exception as e:
            self.exceptCount += 1
            print(str(self.exceptCount))
            TimedAnimation._stop(self)
            pass
        return

    def getYLims(self):
        return self.ax1.get_ylim()

    def _draw_frame(self, framedata):
        margin = 2
        while(len(self.addedData) > 0):
            self.y = np.roll(self.y, -1)
            self.y[-1] = self.addedData[0]
            del(self.addedData[0])

        self.line1.set_data(self.n[ 0 : self.n.size - margin ], self.y[ 0 : self.n.size - margin ])
        self.line1_tail.set_data(np.append(self.n[-10:-1 - margin], self.n[-1 - margin]), np.append(self.y[-10:-1 - margin], self.y[-1 - margin]))
        self.line1_head.set_data(self.n[-1 - margin], self.y[-1 - margin])
        self._drawn_artists = [self.line1, self.line1_tail, self.line1_head]
        return
