#!/usr/bin/python3.6
# coding: utf-8

from PyQt5 import QtWidgets,uic
import numpy as np
import epics
from ecmcArrayStat import *
from ecmcOneMotorGUI import *
from ecmcMainWndDesigner import Ui_MainWindow
import ecmcTrendPv

# Needed packages:
# 1. sudo yum -y install https://rhel7.iuscommunity.org/ius-release.rpm
# 2. sudo pip3.6 install pyqt5
# 3. sudo yum install qt5-qtbase-devel
# 4. sudo python3.6 -m pip install numpy scipy matplotlib
# 5. sudo pip3 install pyepics
# 6. sudo yum install python3-matplotlib


# Regenerate py from ui file:
# pyuic5 -x ecmcMainWndDesigner.ui -o ecmcMainWndDesigner.py

class ecmcMainWindow(QtWidgets.QMainWindow):
  def __init__(self):
    
    super(ecmcMainWindow,self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.ui.pbStartGUI.clicked.connect(self.showGUI)
    self.ui.lineIOCPrefix.textChanged.connect(self.newIOCPrefix)
    self.ui.linepvName.textChanged.connect(self.newIOCpvName)    
    self.prefix=""
    self.pvName=""    
    self.pv=None
    
    if len(sys.argv)>1:
      self.pvPrefix=sys.argv[1]
      self.ui.lineIOCPrefix.setText(self.pvPrefix)
      if len(sys.argv)>2:       
        self.pvName=sys.argv[2]
        self.ui.linepvName.setText(self.pvName)

  def showGUI(self):
    entirePvName = self.prefix+self.pvName    
    pos = entirePvName.rfind('.')
    
    # Check if motor
    if pos < 0:
      pv  = epics.PV(entirePvName + '.RTYP')
      if pv.get() == 'motor':
        self.showMotorGUI(self.pvPrefix, self.pvName)
        return

    # Normal PV
    self.showGuiPv(self.pvPrefix+self.pvName)

  def showMotorGUI(self,pvPrefix,pvName):
    self.dialog = MotorPanel(self,pvPrefix,pvName)
    self.dialog.resize(500, 900)
    self.dialog.show()
    
  def showGuiPv(self, pvName):
    dialog = ecmcTrendPv.ecmcTrendPv(pvName)
    dialog.show()

  def newIOCPrefix(self,iocPrefix):
    self.prefix=iocPrefix

  def newIOCpvName(self,pvName):
    self.pvName=pvName

  def quit(self):
    self.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window=ecmcMainWindow();
    window.show()
    sys.exit(app.exec_())
    