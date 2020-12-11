#!/usr/bin/env python
# Go to Fwd limit and then go back one mm and then again into the switch

import epics
import os
import sys
import time
import math
import unittest
import ecmcSlitDemoLib

testLoops = 10
timeout = 50
if len(sys.argv)!=6:
  print("python ecmcTestHome.py. <motorPvNamepv> <testnumberpv> <sequence> <timout> <testnumber>")
  print("python ecmcTestHome.py IOC:Axis1 IOC:TestNumber 1 50 10")
  sys.exit()


motorPvName = sys.argv[1]
testPvname  = sys.argv[2]
nCmdData = float(sys.argv[3]) 
timeout = float(sys.argv[4]) 
testNumber = float(sys.argv[5]) 
testPv = epics.PV(testPvname)

if testPv is None:
   print ("Invalid testPv") 
   sys.exit()

#Start homing sequences
ecmcSlitDemoLib.setAxisEnable(motorPvName, 1)
time.sleep(1) 
ecmcSlitDemoLib.triggHomeAxis(motorPvName,nCmdData)
time.sleep(1) 
ecmcSlitDemoLib.setAxisEnable(motorPvName, 0)
testPv.put(testNumber)

print ('Homing done')

# Runing homing
