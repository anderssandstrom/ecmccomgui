import epics
import time

import numpy as np

cmds = {}
cmds['exeCmd'] = '-ExeCmd'  # Execute command
cmds['stpCmd'] = '-StpCmd'  # Stop motion
cmds['enaCmd'] = '-EnaCmd'  # Enable command
cmds['enaAct'] = '-EnaAct'  # Enabled status
cmds['tgtPosCmd'] = '-TgtPosCmd'  # Target position
cmds['tgtVelCmd'] = '-TgtVelCmd'  # Target Velocity
cmds['mtnCmd'] = '-MtnCmd'  # "MOVE_ABS", "MOVE_REL", "MOVE_VEL"
cmds['mtnCmdData'] = '-MtnCmdData'  # Param to MtnCmd
cmds['posAct'] = '-PosAct'  # Actual position
cmds['rstCmd'] = '-RstCmd'  # Reset axis
cmds['errId'] = '-ErrId'  # Error ID
cmds['errMsg'] = '-MsgTxt'  # Error Message
cmds['moving'] = '-Moving'  # moving flag
cmds['busy'] = '-Busy'  # busy flag


class Axis:
    def __init__(self, motorPrefix):
        self.motorPrefix = motorPrefix
        self.PVs = {}
        self.enabled = False
        self.busy = False
        self.errId = 0
        self.target = 0
        self.velocity = 0
        self.position = 0
        self.dtg = 0

    def enaCb(self, pvname=None, value=None, char_value=None, **kw):
        self.enabled = value

    def errorIdCb(self, pvname=None, value=None, char_value=None, **kw):
        self.errId = value

    def busyCb(self, pvname=None, value=None, char_value=None, **kw):
        self.busy = value

    def posCb(self, pvname=None, value=None, char_value=None, **kw):
        self.position = value
        self.dtg = self.target - self.position

    def linkPVs(self):
        for key, cmd in cmds.items():
            self.PVs[key] = epics.PV(self.motorPrefix + cmd)

        if None in self.PVs.values():
            raise RuntimeError("failed to connect some PVs.")
        # add callbacks
        self.PVs['enaAct'].add_callback(self.enaCb)
        self.PVs['errId'].add_callback(self.errorIdCb)
        self.PVs['busy'].add_callback(self.busyCb)
        self.PVs['posAct'].add_callback(self.posCb)

    def setCmd(self, type_='MOVE_ABS'):
        print(f'Set motion mode to {type_}:')
        self.PVs['mtnCmd'].put(type_, wait=True, timeout=5)
        self.PVs['mtnCmdData'].put(0, wait=True, timeout=5)

    def disable(self):
        if self.enabled:
            self.PVs['enaCmd'].put(0, wait=True, timeout=5)
            self.forceOff()

    def enable(self):
        if not self.enabled:
            self.PVs['enaCmd'].put(1, wait=True, timeout=5)
            self.forceOn()

    def forceOff(self):
        t0 = time.time()
        while time.time() - t0 < 1.0:
            time.sleep(1.e-3)
            if not self.enabled:
                print(f'Disabled amplifier of {self.motorPrefix}')
                return 0
        raise RuntimeError('failed to disable Amp!')

    def forceOn(self):
        t0 = time.time()
        while time.time() - t0 < 1.0:
            time.sleep(1.e-3)
            if self.enabled:
                print(f'Enabled amplifier of {self.motorPrefix}')
                return 0
        raise RuntimeError('failed to enable Amp!')

    def resetErr(self):
        t0 = time.time()
        self.PVs['rstCmd'].put(1, wait=True, timeout=5)
        while time.time() - t0 < 1.0:
            time.sleep(1.e-3)
            if self.errId == 0:
                print(f'Error reset complete for {self.motorPrefix}')
                return 0
        self.PVs['rstCmd'].put(0, wait=True, timeout=5)
        raise RuntimeError('failed to reset errors')

    def resetExe(self):
        self.PVs['exeCmd'].put(0, wait=True, timeout=5)

    def execute(self):
        try:
            assert self.errId == 0
            self.PVs['exeCmd'].put(1, wait=True, timeout=5)
            self.PVs['exeCmd'].put(0, wait=True, timeout=5)
        except AssertionError:
            raise AssertionError(f'axis {self.motorPrefix} is in error state!')

    def stop(self):
        self.PVs['stpCmd'].put(1, wait=True, timeout=5)
        self.PVs['stpCmd'].put(0, wait=True, timeout=5)

    def checkErrId(self):
        errorId = self.PVs['errId'].get(timeout=5)
        if errorId is None:
            raise RuntimeError('failed to get errorId')

        if errorId:
            errorMsg = self.PVs['errMsg'].get(timeout=5)
            self.stop()
            self.disable()
            raise RuntimeError(f'Axis in error state: {errorId} --> {errorMsg}')

    def setTarget(self, target=None):
        self.target = target if not None else self.target
        self.PVs['tgtPosCmd'].put(target)

    def setVelocity(self, velocity=None, uni=True):
        self.velocity = velocity if not None else self.velocity
        self.PVs['tgtVelCmd'].put(velocity)

    def getReady(self):
        self.disable()
        self.resetErr()
        self.resetExe()
        self.enable()
        self.stop()
        self.checkErrId()


if __name__ == '__main__':
    axis = Axis('n4003:M1')
    axis.linkPVs()
    axis.resetErr()
