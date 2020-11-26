#!/usr/bin/python
# coding: utf-8
import sys
from PyQt4 import QtGui
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
import epics
import positionFFTGUI as GUI


#main=GUI.Main();

def main():
  print "2"
  app = QtGui.QApplication(sys.argv)
  main=GUI.Main();
  main.show()
  sys.exit(app.exec_())

if __name__ == '__main__':
  print "1"
  main()
