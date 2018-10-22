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
        MainWindow.resize(454, 418)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.linePvName = QtWidgets.QLineEdit(self.centralwidget)
        self.linePvName.setObjectName("linePvName")
        self.gridLayout.addWidget(self.linePvName, 3, 0, 1, 1)
        self.btnStart = QtWidgets.QPushButton(self.centralwidget)
        self.btnStart.setObjectName("btnStart")
        self.gridLayout.addWidget(self.btnStart, 0, 0, 1, 1)
        self.pbStartMotorGUI = QtWidgets.QPushButton(self.centralwidget)
        self.pbStartMotorGUI.setObjectName("pbStartMotorGUI")
        self.gridLayout.addWidget(self.pbStartMotorGUI, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 454, 28))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ECMC"))
        self.btnStart.setText(_translate("MainWindow", "Start"))
        self.pbStartMotorGUI.setText(_translate("MainWindow", "Open Motor GUI"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))

