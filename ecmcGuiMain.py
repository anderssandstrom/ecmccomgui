#!/usr/bin/python3.6
# coding: utf-8

from PyQt5 import QtWidgets
import numpy as np
import epics
from ecmcArrayStat import *
from ecmcOneMotorGUI import *
from ecmcMainWndDesigner import Ui_MainWindow

# Needed packages:
# 1. sudo yum -y install https://rhel7.iuscommunity.org/ius-release.rpm
# 2. sudo pip3.6 install pyqt5
# 3. sudo yum install qt5-qtbase-devel
# 4. sudo python3.6 -m pip install numpy scipy matplotlib
# 5. sudo pip3 install pyepics

# Regenerate py from ui file:
# pyuic5 ecmcMainWndDesigner.ui -o ecmcMainWndDesigner.py

# run with python3.6 ecmcGuiMain.py

class ecmcMainWindow(QtWidgets.QMainWindow):
  def __init__(self):
    super(ecmcMainWindow,self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.ui.btnStart.clicked.connect(self.start)
    self.ui.pbStartMotorGUI.clicked.connect(self.showMotorGUI)
    self.ui.linePvName.textChanged.connect(self.newPV)
    self.diagPvName=""
    self.motorPvName=""
    print(sys.argv)
    if(len(sys.argv)>1):
      self.newPV(sys.argv[1])
      self.ui.linePvName.setText(self.motorPvName)
      self.motorPv = epics.PV(self.motorPvName)
      self.diagPv = epics.PV(self.diagPvName)
      print("####################MOTOR####################")
      print(self.motorPv.get())
      print(self.motorPv.count, self.motorPv.type)
      print(self.motorPv.info)
      print("####################DIAG#####################")
      print(self.diagPv.get())
      print(self.diagPv.count, self.diagPv.type)
      print(self.diagPv.info)

      self.arrayStat=ecmcArrayStat()      

  def showMotorGUI(self):
    self.dialog = MotorPanel(self,self.motorPvName)
    self.dialog.resize(200, 100)
    self.dialog.show()

  def newPV(self,pvName):
    self.diagPvName=pvName+"-Array-Stat"
    self.motorPvName=pvName

  def start(self):  
    self.diagPv.add_callback(self.onChanges)

  def paus(self):
    self.diagPv.clear_callbacks()
 
  def onChanges(self,pvname=None, value=None, char_value=None, **kw):
    errorCode=self.arrayStat.parseAxisStatArray(char_value)
    if errorCode:
      print("Parse failed with error code: " + str(errorCode))
    print(self.arrayStat.printInfo())

  def quit(self):
    self.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window=ecmcMainWindow();
    window.show()
    sys.exit(app.exec_())