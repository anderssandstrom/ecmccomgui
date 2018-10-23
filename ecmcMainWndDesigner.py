# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ecmcMainWndDesigner.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(454, 251)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.lblPrefix = QtWidgets.QLabel(self.centralwidget)
        self.lblPrefix.setObjectName("lblPrefix")
        self.gridLayout.addWidget(self.lblPrefix, 0, 0, 1, 1)
        self.pbStartMotorGUI = QtWidgets.QPushButton(self.centralwidget)
        self.pbStartMotorGUI.setObjectName("pbStartMotorGUI")
        self.gridLayout.addWidget(self.pbStartMotorGUI, 5, 0, 1, 1)
        self.lineAxisName = QtWidgets.QLineEdit(self.centralwidget)
        self.lineAxisName.setObjectName("lineAxisName")
        self.gridLayout.addWidget(self.lineAxisName, 4, 0, 1, 1)
        self.lineIOCPrefix = QtWidgets.QLineEdit(self.centralwidget)
        self.lineIOCPrefix.setObjectName("lineIOCPrefix")
        self.gridLayout.addWidget(self.lineIOCPrefix, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
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
        self.lblPrefix.setText(_translate("MainWindow", "IOC Prefix:"))
        self.pbStartMotorGUI.setText(_translate("MainWindow", "Open Motor GUI"))
        self.label.setText(_translate("MainWindow", "Axis Name:"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))

