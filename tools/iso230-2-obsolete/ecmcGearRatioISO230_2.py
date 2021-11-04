#!/usr/bin/python
# coding: utf-8
import sys
import numpy as np
from ecmcISO230_2 import *

def printOutHelp():
  print ("python ecmcGearRatioISO230.py <filename>]")
  print ("example: python ecmcGearRatioISO230.py data.log")
  print ("example stdin: cat data.log | python ecmcGearRatio.py" )
  print ("Ouputs z0 z1 datacount residual")

def main():   
  if len(sys.argv ) > 2 :  
      printOutHelp()
      sys.exit()

  if len(sys.argv)==2:
    fname=sys.argv[1]

  if len(sys.argv)==1:
    fname=""
    
  iso = ecmcISO230_2()
  iso.loadFile(fname)
  [gr,off,count,res]=iso.calcGearRatio()
  # Output
  print (str(gr) + " " + str(off) + " "+ str(count) + " "+ str(res))
  
if __name__ == "__main__":
  main()
