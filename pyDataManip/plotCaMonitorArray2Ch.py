#!/usr/bin/python
# coding: utf-8
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from caPVArrayLib import caPVArray
from caMonitorArrayParserLib import caMonitorArrayParser 
import numpy, scipy
from scipy.signal import correlate

def printOutHelp():
  print("python plotCaMonitor.py [<filename>]")
  print("example: python plotCaMonitor.py xx.txt")
  print("example stdin: cat data.log | grep -E 'thread|CPU' | python plotCaMonitor.py")

def main():
  # Check args
  if len(sys.argv)>1:
    print(sys.argv[1])
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
  dataBuffer01=np.array([])
  dataBuffer02=np.array([])
  counter=0
  counter2=0
  for line in dataFile:
    if not parser.lineValid(line):      
      continue

    pvName, timeVal, data=parser.getValues(line)
  
    if pvName.find("01")>0:

      dataBuffer01=np.append(dataBuffer01,data[:].astype(np.float))
      
    if pvName.find("02")>0:
      #if counter2>2:
      dataBuffer02=np.append(dataBuffer02,data[:].astype(np.float))
      #counter2+=1

    counter+=1
    print("Row: " + str(counter))
  
  
  plt.plot(dataBuffer01)
  plt.plot(dataBuffer02)  
  plt.grid()
  plt.title("Wavform data")
  plt.xlabel("Samples")
  plt.ylabel("Voltage [raw]")
  #plt.show()
  

  #corr=np.correlate(dataBuffer01, dataBuffer02)
  #print('Corr: '+ str(corr))


  nsamples = dataBuffer01.size
  
  # regularize datasets by subtracting mean and dividing by s.d.
  dataBuffer01 -= dataBuffer01.mean(); dataBuffer01 /= dataBuffer01.std()
  dataBuffer02 -= dataBuffer02.mean(); dataBuffer02 /= dataBuffer02.std()
  
  # Find cross-correlation
  xcorr = correlate(dataBuffer01, dataBuffer02)
  
  # delta time array to match xcorr
  dt = numpy.arange(1-nsamples, nsamples)
  
  recovered_time_shift = dt[xcorr.argmax()]
  
  print ("Sample shift: "  + str(recovered_time_shift)  )
  plt.show()

if __name__ == "__main__":
  main()
