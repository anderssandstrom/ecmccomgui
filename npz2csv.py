#*************************************************************************
# Copyright (c) 2020 European Spallation Source ERIC
# ecmc is distributed subject to a Software License Agreement found
# in file LICENSE that is included with this distribution. 
#
#   npz2csv.py
#
#  Created on: October 14, 2020
#      Author: Anders Sandström
#    
#  Converts npz file to csv files
#  
#*************************************************************************

import sys
import numpy as np

def printOutHelp():
  print("npz2csv: Converts npz file to csv files. ")
  print("python npz2csv.py  <filename.npz>")
  print("example: python npz2csv.py data.npz")
  return

def openAndConvert(npzfilename):    
  npzfile = np.load(npzfilename)
  # verify scope plugin
  if npzfile is None:
    print("Input file: " + npzfilename + " not valid.")
    return
  
  outfilenameinfo = npzfilename.split('.')[0] + ".info.csv"
  firstInfoWrite = True
  for file in npzfile.files:
    print("Handling file:" + file)

    outfilename = npzfilename.split('.')[0] + "." + file + ".csv"
    
    if np.size(npzfile[file]) == 1:
      if firstInfoWrite:
        f = open(outfilenameinfo,'wt')
        firstInfoWrite = False
      else:
        f = open(outfilenameinfo,'at')
      f.write(file + "=" + str(npzfile[file])+'\n')
      f.close()
    else:
      outfilename = npzfilename.split('.')[0] + "." + file + ".csv"
      np.savetxt(outfilename,np.array(npzfile[file]), delimiter=",")
  return

if __name__ == "__main__":  
  if len(sys.argv)!=2:
    printOutHelp()
    sys.exit()
  
  npzfilename=sys.argv[1]
  
  if npzfilename is None:
    print("Input file: " + npzfilename + " not valid.")
    sys.exit()
  
  openAndConvert(npzfilename)

  