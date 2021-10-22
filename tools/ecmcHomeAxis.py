#!/usr/bin/env python

import epics
import os
import sys
import time
import math
import unittest
import ecmcSlitDemoLib

if len(sys.argv)!=3:
  print( "python2 ecmcHomeAxis.py <motorpv> <home seq num>")
  print( "python2 ecmcHomeAxis.py IOC:Axis1 3")
  sys.exit()

motor = sys.argv[1]
nCmdData = int(sys.argv[2])

homedPvSuffix='-Homed'
motorHomedPvName = motor + homedPvSuffix
homedPv = epics.PV(motorHomedPvName)

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

#Start homing sequences
ecmcSlitDemoLib.triggHomeAxis(motor,nCmdData)

ecmcSlitDemoLib.setAxisEnable(motor, 0)

print ('Homing done')

