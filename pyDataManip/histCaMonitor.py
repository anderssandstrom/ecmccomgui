#!/usr/bin/python
# coding: utf-8
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from datetime import datetime
from caPVArrayLib import caPVArray
from caMonitorArrayParserLib import caMonitorArrayParser 

def printOutHelp():
  print("python plotCaMonitor.py [<filename>]")
  print("example: python plotCaMonitor.py xx.txt")
  print("example stdin: cat data.log | grep -E 'thread|CPU' | python plotCaMonitor.py")

def main():
  # Check args
  if len(sys.argv)>1:
    print (sys.argv[1])
    pos1=sys.argv[1].find('-h')
    if(pos1>=0):
      printOutHelp()
      sys.exit()
    pos1=sys.argv[1].find('-t')
    if(pos1>=0) and len(sys.argv)>2:
      title = sys.argv[2]
      if len(sys.argv)>3:
        fname=sys.argv[3]
        dataFile=open(fname,'r')
      else:
        fname=""      
        dataFile=sys.stdin
    else:
      title=""
      fname=sys.argv[2]
      dataFile=open(fname,'r')
  else:
    title=""
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
      print("Added PV: " + pvName)
  
  print("Statistics: ")
  legend=[]
  count=0
  for pv in pvs: 
    
    count+=1
    timeSet, dataSet=pv.getData()     
    #for d in dataSet:
    #  print(d)
    pvLength = pv.getLength()    
    pvMax = np.max(dataSet)
    pvMin = np.min(dataSet)
    pvAvg = np.mean(dataSet)
    pvStd = np.std(dataSet)
    legStr = pv.getName() + "[" + str(pvLength) + "] " + str(pvMin) + ".." + str(pvMax) + ", mean: " + str(pvAvg) + ", std: " + str(pvStd) + ", range: " +str(pvMax-pvMin)
    #infoStr = "[" + str(pvLength) + "] " + str(pvMin) + ".." + str(pvMax) + ", mean: " + str(pvAvg) + ", std: " + str(pvStd) + ", range: " +str(pvMax-pvMin)
    infoStr = pv.getName() + "[{0}]:\n  range: {1:.7f}.. {2:.7f} ({3:.7f}), \n  mean: {4:.7f},\n  std: {5:.7f}".format(pvLength, pvMin,pvMax,pvMax-pvMin,pvAvg,pvStd)
    legend.append(pv.getName())
     
    x=timeSet
    
    print(legStr)
    plt.figure(figsize=(8, 8))
    n, bins, patches = plt.hist(dataSet, int(pvLength/5), density=1)
    y = mlab.normpdf( bins, pvAvg, pvStd)
    l = plt.plot(bins, y, linewidth=1) 

  if count == 1:    
    plt.gcf().text(0.01,0.91,infoStr) 

  plt.legend(legend)
  plt.grid()
  plt.title(title)
  plt.show()


if __name__ == "__main__":
  main()
