import numpy as np

PARSE_ERROR_ELEMENT_COUNT_OUT_OF_RANGE = 1000
ELEMENT_COUNT = 30

class ecmcArrayStat:
  def __init__(self):
    self.axId=0
    self.posSet=0
    self.posAct=0
    self.posErr=0
    self.posTarg=0
    self.posErrTarg=0
    self.posRaw=0
    self.cntrlOut=0
    self.velSet=0
    self.velAct=0
    self.velFFraw=0
    self.velRaw=0
    self.cycleCounter=0
    self.error=0
    self.command=0
    self.cmdData=0
    self.seqState=0
    self.ilock=0
    self.ilockLastActive=0
    self.trajSource=0
    self.encSource=0
    self.enable=0
    self.enabled=0
    self.execute=0
    self.busy=0
    self.atTarget=0
    self.homed=0
    self.lowLim=0
    self.highLim=0
    self.homeSensor=0
    return

  def parseAxisStatArray(self,charData):
    dataList=charData.split(',')
    if len(dataList)!=ELEMENT_COUNT:
      return PARSE_ERROR_ELEMENT_COUNT_OUT_OF_RANGE

    self.axId=int(dataList[0])
    self.posSet=float(dataList[1])
    self.posAct=float(dataList[2])
    self.posErr=float(dataList[3])
    self.posTarg=float(dataList[4])
    self.posErrTarg=float(dataList[5])
    self.posRaw=float(dataList[6])
    self.cntrlOut=float(dataList[7])
    self.velSet=float(dataList[8])
    self.velAct=float(dataList[9])
    self.velFFraw=float(dataList[10])
    self.velRaw=float(dataList[11])
    self.cycleCounter=int(dataList[12])
    self.error=int(dataList[13])
    self.command=int(dataList[14])
    self.cmdData=int(dataList[15])
    self.seqState=int(dataList[16])
    self.ilock=int(dataList[17])
    self.ilockLastActive=int(dataList[18])
    self.trajSource=int(dataList[19])
    self.encSource=int(dataList[20])
    self.enable=int(dataList[21])
    self.enabled=int(dataList[22])
    self.execute=int(dataList[23])
    self.busy=int(dataList[24])
    self.atTarget=int(dataList[25])
    self.homed=int(dataList[26])
    self.lowLim=int(dataList[27])
    self.highLim=int(dataList[28])
    self.homeSensor=int(dataList[29])
    return

  def printInfo(self):
    print("axId             :  " + str(self.axId))
    print("posSet           :  " + str(self.posSet))
    print("posAct           :  " + str(self.posAct))
    print("posErr           :  " + str(self.posErr))
    print("posTarg          :  " + str(self.posTarg))
    print("posErrTarg       :  " + str(self.posErrTarg))
    print("posRaw           :  " + str(self.posRaw))
    print("cntrlOut         :  " + str(self.cntrlOut))
    print("velSet           :  " + str(self.velSet))
    print("velAct           :  " + str(self.velAct))
    print("velFFraw         :  " + str(self.velFFraw))
    print("velRaw           :  " + str(self.velRaw))
    print("cycleCounter     :  " + str(self.cycleCounter))
    print("error            :  " + str(self.error))
    print("command          :  " + str(self.command))
    print("cmdData          :  " + str(self.cmdData))
    print("seqState         :  " + str(self.seqState))
    print("ilock            :  " + str(self.ilock))
    print("ilockLastActive  :  " + str(self.ilockLastActive))
    print("trajSource       :  " + str(self.trajSource))
    print("encSource        :  " + str(self.encSource))
    print("enable           :  " + str(self.enable))
    print("enabled          :  " + str(self.enabled))
    print("execute          :  " + str(self.execute))
    print("busy             :  " + str(self.busy))
    print("atTarget         :  " + str(self.atTarget))
    print("homed            :  " + str(self.homed))
    print("lowLim           :  " + str(self.lowLim))
    print("highLim          :  " + str(self.highLim))
    print("homeSensor       :  " + str(self.homeSensor))
    return
