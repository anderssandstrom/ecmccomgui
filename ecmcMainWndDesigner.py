# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ecmcMainWndDesigner.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(929, 310)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pvLayout = QtWidgets.QVBoxLayout()
        self.pvLayout.setObjectName("pvLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.pvLayout.addWidget(self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.pvLayout.addWidget(self.lineEdit)
        self.pbStartpvTrend = QtWidgets.QPushButton(self.centralwidget)
        self.pbStartpvTrend.setObjectName("pbStartpvTrend")
        self.pvLayout.addWidget(self.pbStartpvTrend)
        self.horizontalLayout.addLayout(self.pvLayout)
        self.motorLayout = QtWidgets.QVBoxLayout()
        self.motorLayout.setObjectName("motorLayout")
        self.lblPrefix = QtWidgets.QLabel(self.centralwidget)
        self.lblPrefix.setObjectName("lblPrefix")
        self.motorLayout.addWidget(self.lblPrefix)
        self.lineIOCPrefix = QtWidgets.QLineEdit(self.centralwidget)
        self.lineIOCPrefix.setObjectName("lineIOCPrefix")
        self.motorLayout.addWidget(self.lineIOCPrefix)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.motorLayout.addWidget(self.label)
        self.lineAxisName = QtWidgets.QLineEdit(self.centralwidget)
        self.lineAxisName.setObjectName("lineAxisName")
        self.motorLayout.addWidget(self.lineAxisName)
        self.pbStartMotorGUI = QtWidgets.QPushButton(self.centralwidget)
        self.pbStartMotorGUI.setObjectName("pbStartMotorGUI")
        self.motorLayout.addWidget(self.pbStartMotorGUI)
        self.horizontalLayout.addLayout(self.motorLayout)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ECMC"))
        self.label_2.setText(_translate("MainWindow", "PV name:"))
        self.pbStartpvTrend.setText(_translate("MainWindow", "Open PV Trend"))
        self.lblPrefix.setText(_translate("MainWindow", "IOC Prefix:"))
        self.label.setText(_translate("MainWindow", "Axis Name:"))
        self.pbStartMotorGUI.setText(_translate("MainWindow", "Open Motor GUI"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

