#!/usr/bin/env python
# Go to Fwd limit and then go back one mm and then again into the switch

import epics
import os
import sys
import time
import math
import unittest
import ecmcSlitDemoLib

if len(sys.argv)!=2:
  print("python ecmcTestInit.py <testnumberpv>")
  print("python ecmcTestInit.py IOC:TestNumber")
  sys.exit()

testPvname  = sys.argv[1]
testPv = epics.PV(testPvname)

if testPv is None:
   print ("Invalid testPv") 
   sys.exit()

testPv.put(0)

print ('Init done')
