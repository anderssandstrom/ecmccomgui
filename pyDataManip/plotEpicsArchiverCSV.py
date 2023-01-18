#!/usr/bin/python
# coding: utf-8
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
 
def printOutHelp():
  print ("python plotEpicsArchiverCSV.py [<filename>]")
  print ("example: python plotEpicsArchiverCSV.py xx.txt")
  print ("example stdin: cat data.log | grep -E 'thread|CPU' | python plotEpicsArchiverCSV.py" )

def main():
  # Check args
  if len(sys.argv)>1:
    print(sys.argv[1] )
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
    dataFile=sys.stdin;
  
  y=np.array([])
  x=np.array([])
  cc=0
  # Seconds   , value, alarm state, alarm severity, nanoseconds   
  # 1670828407,-0.1,0,0,13856621
  for line in dataFile:
    
    newLine = line.replace(",", " ")
    newList = newLine.split()
    if len(newList)!=5:
      print("Invalid line: " + line)
      continue
    cc=cc+1
    print (cc)
    # add nanos to seconds (epoch)
    timeStampStr = newList[0] + "." + newList[4]
    dataStr = newList [1]
    dataValue = float(dataStr)
    y = np.append(y,dataValue)
    timeValue = datetime.fromtimestamp( float(timeStampStr ))
    x = np.append(x,timeValue)
  
  print("Statistics: ")
  #for d in dataSet:
  #  print d
  pvLength = len(y)
  pvMax = np.max(y)
  pvMin = np.min(y)
  pvAvg = np.mean(y)
  pvStd = np.std(y)
  legStr = "[" + str(pvLength) + "] " + str(pvMin) + ".." + str(pvMax) + ", mean: " + str(pvAvg) + ", std: " + str(pvStd)
  #legend.append(filename)
   
  print (legStr)
  plt.plot(x,y,'o-')

  #plt.legend(legStr)
  plt.grid()
  plt.title(fname)
  plt.xlabel("time")
  plt.show()
  
if __name__ == "__main__":
  main()
