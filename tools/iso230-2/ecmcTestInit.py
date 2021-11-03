#!/usr/bin/env python
# Go to Fwd limit and then go back one mm and then again into the switch

import epics
import os
import sys
import time
import math
import unittest
import ecmcSlitDemoLib

if len(sys.argv)!=3:
  print("python ecmcTestInit.py <testnumberpv> <numberToSet>")
  print("python ecmcTestInit.py IOC:TestNumber 10")
  sys.exit()

testPvname  = sys.argv[1]
testPv = epics.PV(testPvname)
testNumber  = float(sys.argv[2]) 

if testPv is None:
   print ("Invalid testPv") 
   sys.exit()

testPv.put(testNumber)

print ('Init done')
