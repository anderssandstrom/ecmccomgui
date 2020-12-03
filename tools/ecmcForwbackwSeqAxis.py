#!/usr/bin/env python

import epics
import os
import sys
import time
import math
import unittest
import ecmcSlitDemoLib

if len(sys.argv)!=5:
  print("python2 ecmcForwbackSeq.py <motorpv> <from pos> <to pos> <velo>")
  print("python2 ecmcForwbackSeq.py IOC:Axis1 0 100 25")
  sys.exit()


motor = sys.argv[1]
fromPos = float(sys.argv[2])
toPos = float(sys.argv[3])
velo  = float(sys.argv[4]) 

maxPos = toPos
if fromPos > maxPos:
  maxPos = fromPos

minPos = fromPos
if toPos < minPos:
  minPos = toPos

#Disable softLimits
print( 'Set softlimits')
ecmcSlitDemoLib.setSoftLowLimt(motor, minPos -10)
ecmcSlitDemoLib.setSoftHighLimt(motor, maxPos +10)

print ('Disable amplifier')
ecmcSlitDemoLib.setAxisEnable(motor, 0)
time.sleep(1) #ensure that enabled goes down
error=ecmcSlitDemoLib.getAxisError(motor,1)

#Reset error on all axis
print ('Reset error axes.')
ecmcSlitDemoLib.setAxisReset(motor, 1)
time.sleep(0.5)
ecmcSlitDemoLib.setAxisReset(motor, 0)

print ('Enable amplifier')
ecmcSlitDemoLib.setAxisEnable(motor, 1)
time.sleep(1) #ensure that enabled goes down
error=ecmcSlitDemoLib.getAxisError(motor,1)
counter = 0;

timeOut = (maxPos-minPos)/velo*1.5

while 1:
  #run gap and center motor to 0
  print ('Move axis to position ' + str(fromPos) + ' (cycles = ' + str(counter) + ').')
  done=ecmcSlitDemoLib.moveAxisPosition(motor,fromPos,velo,timeOut)
  if not done:
    print (motor + " failed to position.")
    sys.exit()

  print ('Move axis to position ' + str(toPos) + ' (cycles = ' + str(counter) + ').')
  done=ecmcSlitDemoLib.moveAxisPosition(motor,toPos,velo,timeOut)
  if not done:
    print( motor + " failed to position.")
    sys.exit()
  counter = counter +1
