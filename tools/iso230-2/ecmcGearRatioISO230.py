#!/usr/bin/python
# coding: utf-8
import sys
import numpy as np
import ecmcISO230_2 as iso230

def printOutHelp():
  print ("python ecmcGearRatioISO230.py <filename>]")
  print ("example: python ecmcGearRatioISO230.py data.log")
  print ("example stdin: cat data.log | python ecmcGearRatio.py" )
  print ("Ouputs z0 z1 datacount residual")

def main():   
  if len(sys.argv ) > 4 or len(sys.argv) < 3  :  
      printOutHelp()
      sys.exit()

  fromPvNameFilter = sys.argv[1]
  toPvNameFilter = sys.argv[2]

#  print("Initiating calculation of gear ration between "+ fromPvNameFilter + " and " +toPvNameFilter)

  if len(sys.argv)==2:
    fname=sys.argv[1]

  if len(sys.argv)==1:
    fname=""

  iso=iso230()
  iso.loadFile(fname)
  [gr,off,count,res]=iso.calcGearRatio()
  # Output
  print (str(gr) + " " + str(off) + " "+ str(count) + " "+ str(res))
  
if __name__ == "__main__":
  main()
