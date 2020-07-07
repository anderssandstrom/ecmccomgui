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

    self.ui.comboPrefix.currentIndexChanged.connect(self.newPrefixComboIndex)
    self.ui.comboPrefix.addItem("IOC_TEST:")
    self.ui.comboPrefix.addItem("IOC:")
    self.ui.comboPrefix.addItem("IOC2:")
    self.ui.comboPrefix.addItem("IOC_SLIT:")
    self.ui.comboPrefix.setToolTip("Predefined IOC prefix. Choose one to use..")

    self.ui.comboPvName.currentIndexChanged.connect(self.newPvComboIndex)
    self.ui.comboPvName.addItem("Axis1")
    self.ui.comboPvName.addItem("Axis2")
    self.ui.comboPvName.addItem("MCU-thread-latency-max")
    self.ui.comboPvName.addItem("MCU-thread-latency-min")
    self.ui.comboPvName.addItem("MCU-thread-period-max")
    self.ui.comboPvName.addItem("MCU-thread-period-min")
    self.ui.comboPvName.addItem("MCU-thread-send-max")
    self.ui.comboPvName.addItem("MCU-thread-send-min")
    self.ui.comboPvName.addItem("ec0-domainfailcountertotal")
    self.ui.comboPrefix.setToolTip("Predefined pv names. Choose one to use..")

    self.prefix=""
    self.pvName=""    
    self.pv=None
    
    if len(sys.argv)>1:
      self.prefix=sys.argv[1]
      self.ui.lineIOCPrefix.setText(self.prefix)
      if len(sys.argv)>2:       
        self.pvName=sys.argv[2]
        self.ui.linepvName.setText(self.pvName)

  def showGUI(self):
    self.prefix=self.ui.lineIOCPrefix.text()
    self.pvName=self.ui.linepvName.text()
    entirePvName = self.prefix+self.pvName
    pos = entirePvName.rfind('.')
    
    # Check if motor
    if pos < 0:
      pv  = epics.PV(entirePvName + '.RTYP')
      if pv.get() == 'motor':
        self.showMotorGUI(self.prefix, self.pvName)
        return

    # Normal PV
    self.showGuiPv(self.prefix+self.pvName)

  def showMotorGUI(self,prefix,pvName):
    self.dialog = MotorPanel(self,prefix,pvName)
    self.dialog.resize(500, 900)
    self.dialog.show()
    
  def showGuiPv(self, pvName):
    dialog = ecmcTrendPv.ecmcTrendPv(pvName)
    dialog.show()

  def newIOCPrefix(self,iocPrefix):
    self.prefix=iocPrefix

  def newIOCpvName(self,pvName):
    self.pvName=pvName

  def newPrefixComboIndex(self,index):
    self.prefix=self.ui.comboPrefix.itemText(index)
    self.ui.lineIOCPrefix.setText(self.prefix)

  def newPvComboIndex(self,index):    
    self.pvName=self.ui.comboPvName.itemText(index)
    self.ui.linepvName.setText(self.pvName)

  def quit(self):
    self.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window=ecmcMainWindow();
    window.show()
    sys.exit(app.exec_())
    