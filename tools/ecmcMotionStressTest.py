#!/usr/bin/env python

import sys
import time
import numpy as np
from random import *
from EcmcAxis import cmds, Axis

'''
    simple CLI, fails if too little args are give, excess args are omitted
    TODO: use argparse for cli
'''
class StressTestCLI:
    def __init__(self):
        try:
            self.me = sys.argv[0]
            self.motorPrefix = sys.argv[1]
            self.minPos = float(sys.argv[2])
            self.maxPos = float(sys.argv[3])
            self.maxVel = float(sys.argv[4])
        except IndexError:
            raise IndexError(f'\npython {self.me} <motor_pv_prefix> <min_pos> <max_pos> <max_velo>\n')

    def report(self):
        print(f'------------------------------------------------------------------------------------------------------')
        print(f'script:      {self.me}')
        print(f'motorPrefix: {self.motorPrefix}')
        print(f'minPos:      {self.minPos}')
        print(f'maxPos:      {self.maxPos}')
        print(f'maxVel:      {self.maxVel}')
        print(f'------------------------------------------------------------------------------------------------------')


class StressTest(Axis):
    def __init__(self, motorPrefix, minPos, maxPos, maxVel):
        super().__init__(motorPrefix)
        self.minPos = minPos
        self.maxPos = maxPos
        self.maxVel = maxVel
        self.counter = 1
        self.maxTime = (self.maxPos - self.minPos) / self.maxVel
        self.timeToWait = 1

    def counterInc(self, inc=1):
        self.counter += inc

    def setTarget(self, target=None, uni=True):
        target = uniform(self.minPos, self.maxPos) if uni else target
        self.target = target if not None else self.target
        self.PVs['tgtPosCmd'].put(target)

    def setVelocity(self, velocity=None, uni=True):
        velocity = uniform(-self.maxVel, self.maxVel) if uni else velocity
        self.velocity = velocity if not None else self.velocity
        self.PVs['tgtVelCmd'].put(velocity)

    def setTimeToWait(self, timeToWait=None, uni=True):
        timeToWait = uniform(0, self.maxTime) if uni else timeToWait
        self.timeToWait = timeToWait if not None else self.timeToWait

    def printInfo(self):
        print(f'Executing new motion cmd no. {self.counter}:')
        print(f'  Busy:             {self.busy}')
        print(f'  Current position: {self.position}')
        print(f'  Target position:  {self.target}')
        print(f'  Target velocity:  {self.velocity}')
        print(f'  Distance to go:   {self.dtg}')
        print(f'  Time to wait (s): {self.timeToWait}')

    def uniformVelocityTargetMoves(self, n=np.Infinity):
        self.setCmd('MOVE_ABS')
        while self.counter < n:
            self.setTarget()
            self.setVelocity()
            self.setTimeToWait()
            self.printInfo()
            self.execute()
            self.counterInc()
            time.sleep(self.timeToWait)


if __name__ == '__main__':
    cli = StressTestCLI()
    cli.report()
    st = StressTest(cli.motorPrefix, cli.minPos, cli.maxPos, cli.maxVel)
    st.linkPVs()
    # prep axis: disable, reset errors, reset execute, enable, stop, check for Errors
    st.getReady()
    # uniform targets and velocity moves, for ever :)
    st.uniformVelocityTargetMoves()

