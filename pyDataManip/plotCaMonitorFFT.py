#!/usr/bin/python
# coding: utf-8
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import scipy.fftpack
from caPVArrayLib import caPVArray
from caMonitorArrayParserLib import caMonitorArrayParser 

def printOutHelp():
  print "python plotCaMonitorFFT.py [<filename>]"
  print "example: python plotCaMonitorFFT.py xx.txt"
  print "example stdin: cat data.log | grep -E 'thread|CPU' | python plotCaMonitorFFT.py" 

def main():
  # Check args
  if len(sys.argv)>1:
    print sys.argv[1] 
    pos1=sys.argv[1].find('-h')
    if(pos1>=0):
      printOutHelp()
      sys.exit()
  
  if len(sys.argv)!=2 and len(sys.argv)>1:  
      printOutHelp()
      sys.exit()
  
  if len(sys.argv)==2:
    fname=sys.argv[1]
    dataFile=open(fname,'r')

  if len(sys.argv)==1:
    fname=""
    dataFile=sys.stdin

  parser=caMonitorArrayParser()
  pvs=[]

  for line in dataFile:
    if not parser.lineValid(line):
      continue

    pvName, timeVal, data=parser.getValues(line)
    newPv=True;
    pvToAddDataTo=caPVArray(pvName)
    # See if old or new pv
    for pv in pvs:
      if pv.getName() == pvName:        
        pvToAddDataTo=pv
        newPv=False;
        break;
    
    pvToAddDataTo.setValues(timeVal,data)
    if newPv:       
      pvs.append(pvToAddDataTo)
      print "Added PV" + pvName
    
  legend=[]
  for pv in pvs: 
    legend.append(pv.getName())
    print  pv.getName()+ ": " + str(pv.getLength())
    timeSet, dataSet = pv.getData() 
    sampleTime=pv.getSampleTime()
    x=timeSet
    y=dataSet
    plt.plot(x,y,'o-')
  
  #print "Sample Mean" + str(np.mean(sampleTime))
  plt.legend(legend)
  plt.grid()
  plt.title(fname)
  plt.xlabel("time")
  
  plt.figure()
  
  
  N = dataSet.size
  # sample spacing
  T = np.mean(sampleTime)
  x = np.linspace(0.0, N*T, N)
  #normalize data (remove slope)  
  p=np.polyfit(x,dataSet,1)
  
  y = dataSet-np.polyval(p,x)
  yf = scipy.fftpack.fft(y)
  xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
  yfft=2.0/N * np.abs(yf[:N//2]) # integer division
  
   
  plt.plot(xf,yfft, '*-')
  plt.grid()
  plt.xlabel("Frequency [Hz]")
  plt.ylabel("Amplitude")
    
  plt.show()
  

  

if __name__ == "__main__":
  main()
    
    
