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
    self.ui.pbStartMotorGUI.clicked.connect(self.showMotorGUI)
    self.ui.lineIOCPrefix.textChanged.connect(self.newIOCPrefix)
    self.ui.lineAxisName.textChanged.connect(self.newIOCAxisName)
    self.prefix=""
    self.axisName=""
    print(sys.argv)
    if len(sys.argv)>1:
      self.prefix=sys.argv[1]
      self.ui.lineIOCPrefix.setText(self.prefix)
      if len(sys.argv)>2:
        self.axisName=sys.argv[2]
        self.ui.lineAxisName.setText(self.axisName)

  def showMotorGUI(self):
    self.dialog = MotorPanel(self,self.prefix,self.axisName)
    self.dialog.resize(400, 800)
    self.dialog.show()
    
  def newIOCPrefix(self,iocPrefix):
    self.prefix=iocPrefix

  def newIOCAxisName(self,axisName):
    self.axisName=axisName

  def quit(self):
    self.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window=ecmcMainWindow();
    window.show()
    sys.exit(app.exec_())