#!/usr/bin/env python

import epics
import os
import sys
import time
import math
import unittest
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack


bufferSize=10000
buffer=np.zeros(10000)
bufferIndex=0
dataPerSample=0;
doFFTSkipCycles=0; 
doFFTSkipCycleCounter=5; 
fig, ax = plt.subplots()
plt.axis()
plt.ion()
plt.show()

def onChanges(pvname=None, value=None, char_value=None, **kw):
    #print 'PV Changed! ', pvname, value, time.ctime()
    global bufferIndex,buffer,dataPerSample,doFFTSkipCycleCounter,doFFTSkipCycles,bufferSize
    dataPerSample=value.size;
    if bufferIndex>=bufferSize:
      buffer.fill(0)
      bufferIndex=0
    buffer[bufferIndex:bufferIndex+value.size]=value;
    bufferIndex=bufferIndex+value.size
    if bufferIndex>=bufferSize:
      print "Buffer Full"
      doFFTSkipCycleCounter=doFFTSkipCycleCounter+1;
      if doFFTSkipCycleCounter>=doFFTSkipCycles:
        doFFTSkipCycleCounter=0
        doFFT(buffer)


def doFFT(data):
    global dataPerSample, fig,ax
    # Number of samplepoints
    N = data.size
    # sample spacing
    T = 1.0 / (dataPerSample*1000)
    x = np.linspace(0.0, N*T, N)
    y = data
    yf = scipy.fftpack.fft(y)
    xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
    yfft=2.0/N * np.abs(yf[:N//2]) # integer division
    ax.cla()
    ax.plot(xf,yfft)
    ax.grid()
    plt.draw()
    plt.ylim([0, 1])
    plt.xlim([0, 20])
    plt.pause(0.001)


pvname='IOC_SLIT:ec0-s10-EL3632_s5-AI1-Array'
#epics.camonitor(pvname)
#time.sleep(1)
#epics.camonitor_clear(pvname)
#from epics import PV
p = epics.PV(pvname) #,auto_monitor=True)
print p.get()
print p.count, p.type
print p.info

mypv = epics.PV(pvname)
mypv.add_callback(onChanges)

#pvname='IOC2:xr-DiagString'
#mypv2 = epics.PV(pvname)
#mypv2.add_callback(onChanges)

#print 'Now wait for changes'

t0 = time.time()
while time.time() - t0 < 60.0:
    time.sleep(1.e-3)
print 'Done.'
