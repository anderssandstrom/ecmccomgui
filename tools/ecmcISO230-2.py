#!/usr/bin/python
# coding: utf-8
import sys
import numpy as np

UNIT="UNIT="
CYCLES="CYCLES="
POSITIONS="POSITIONS"
TGT_DATA="TGT_DATA["
REF_DATA_FWD="REF_DATA_FWD["
REF_DATA_BWD="REF_DATA_BWD["

def printOutHelp():
  print ("python ecmcGearRatecmcISO230-2.py <filename>]")
    
class ecmcISO230_2:
    def __init__(self):
        self.positions = 0
        self.cycles = 0
        self.refData_fwd = {}
        self.refData_bwd = {}
        self.tgtData = {}
        self.unit = ""
        self.x_i_fwd={}
        self.x_i_fwd_avg={}
        self.x_i_bwd={}
        self.x_i_bwd_avg={}
        self.x_i_avg={}
        self.B_i={}
        self.B=0
        self.B_avg=0
        self.s_i_fwd={}
        self.s_i_bwd={}
        self.x_i_j_fwd={}
        self.x_i_j_bwd={}
        self.R_i_fwd={}
        self.R_i_bwd={}
        self.R_i={}
        self.R_fwd=0
        self.R_bwd=0
        self.E_fwd=0
        self.E_bwd=0
        self.E=0
        self.M=0
        self.A_fwd=0
        self.A_bwd=0
        self.A=0

    def parseLine(self, line):
        if line.find(UNIT)>=0:
            self.unit=line.split("=")[1]
            return

        if line.find(CYCLES)>=0:
            self.cycles=int(line.split("=")[1])
            return

        if line.find(POSITIONS)>=0:
            self.positions=int(line.split("=")[1])
            return

        if line.find(REF_DATA_FWD)>=0:
            indexStr=line.split("=")[0]
            indexStr=indexStr.split("[")[1]
            indexStr=indexStr.split("]")[0]
            i=int(indexStr.split(",")[0])
            j=int(indexStr.split(",")[1])
            self.refData_bwd[i,j]=float(line.split("=")[1])
            return

        if line.find(REF_DATA_BWD)>=0:
            indexStr=line.split("=")[0]
            indexStr=indexStr.split("[")[1]
            indexStr=indexStr.split("]")[0]
            i=int(indexStr.split(",")[0])
            j=int(indexStr.split(",")[1])
            self.refData_fwd[i,j]=float(line.split("=")[1])
            return

        if line.find(TGT_DATA)>=0:
            indexStr=line.split("=")[0]
            indexStr=indexStr.split("[")[1]
            i=int(indexStr.split("]")[0])
            self.tgtData[i]=float(line.split("=")[1])
            return

    def calcX(self):
        for i in range(1,self.positions+1):
          x_sum_fwd=0
          x_sum_bwd=0
          
          for j in range(1,self.cycles+1):
            #fwd
            self.x_i_j_fwd[i,j]=self.refData_fwd[i,j]-self.tgtData[i]
            x_sum_fwd+=self.x_i_j_fwd[i,j]
            #bwd
            self.x_i_j_bwd[i,j]=self.refData_bwd[i,j]-self.tgtData[i]
            x_sum_bwd+=self.x_i_j_bwd[i,j]

          self.x_i_fwd_avg[i]=x_sum_fwd/float(self.positions)
          self.x_i_bwd_avg[i]=x_sum_bwd/float(self.positions)
          self.x_i_avg[i]=(self.x_i_fwd_avg[i]+self.x_i_bwd_avg[i])/float(2)
          print("X_fwd_avg" + str(self.x_i_fwd_avg[i]))
          print("X_bwd_avg" + str(self.x_i_bwd_avg[i]))
          print("X_avg" + str(self.x_i_avg[i]))
          
    def calcB(self):
        B_sum=0
        for i in range(1,self.positions+1):
          # B
          self.B_i[i]=self.x_i_fwd_avg[i]-self.x_i_bwd_avg[i]
          B_sum+=self.B_i[i]
          if abs(self.B_i[i])>self.B:
              self.B=abs(self.B_i[i])
        
        self.B_avg=B_sum/float(self.positions)
        print("B_avg="+str(self.B_avg))
        print("B="+str(self.B))

    def calcS(self):
        for i in range(1,self.positions+1):
          s_fwd_tmp_sum=0
          s_bwd_tmp_sum=0  
          for j in range(1,self.cycles+1):
            #fwd
            s_fwd_tmp=(self.x_i_j_fwd[i,j]-self.x_i_fwd_avg[i])
            s_fwd_tmp=s_fwd_tmp*s_fwd_tmp
            s_fwd_tmp_sum+=s_fwd_tmp
            #bwd
            s_bwd_tmp=(self.x_i_j_bwd[i,j]-self.x_i_bwd_avg[i])
            s_bwd_tmp=s_bwd_tmp*s_bwd_tmp
            s_bwd_tmp_sum+=s_bwd_tmp

          self.s_i_fwd[i]=np.sqrt(s_fwd_tmp_sum/float(self.cycles-1))
          self.s_i_bwd[i]=np.sqrt(s_bwd_tmp_sum/float(self.cycles-1))
          print("S_fwd=" + str(self.s_i_fwd[i]))
          print("S_bwd=" + str(self.s_i_bwd[i]))

    def calcR(self):
        self.R_fwd=0
        self.R_bwd=0

        for i in range(1,self.positions+1):
          #fwd
          self.R_i_fwd[i]=4*self.s_i_fwd[i]
          if self.R_i_fwd[i]>self.R_fwd:
              self.R_fwd=self.R_i_fwd[i]
          #bwd
          self.R_i_bwd[i]=4*self.s_i_bwd[i]
          if self.R_i_bwd[i]>self.R_bwd:
              self.R_bwd=self.R_i_fwd[i]

          term1=2*self.s_i_fwd[i] + 2*self.s_i_bwd[i] + np.abs(self.B_i[i])
          term2=self.R_i_fwd[i]
          term3=self.R_i_bwd[i]
          termMax=term1
          if term2>termMax:
              termMax=term2
          if term3>termMax:
              termMax=term3
          self.R_i[i]=termMax

        self.R=self.R_fwd
        if self.R_fwd>self.R:
            self.R=self.R_fwd
            
        print("R_fwd="+ str(self.R_fwd))
        print("R_bwd="+ str(self.R_bwd))
        print("R="+ str(self.R))
          

    def calcE(self):
        x_i_avg_fwd_max=self.x_i_fwd_avg[1]
        x_i_avg_fwd_min=self.x_i_fwd_avg[1]
        x_i_avg_bwd_max=self.x_i_bwd_avg[1]
        x_i_avg_bwd_min=self.x_i_bwd_avg[1]
        for i in range(1,self.positions+1):
          #fwd
          if self.x_i_fwd_avg[i]>x_i_avg_fwd_max:
              x_i_avg_fwd_max=self.x_i_fwd_avg[i]
          if self.x_i_fwd_avg[i]<x_i_avg_fwd_min:
              x_i_avg_fwd_min=self.x_i_fwd_avg[i]

          #bwd
          if self.x_i_bwd_avg[i]>x_i_avg_bwd_max:
              x_i_avg_bwd_max=self.x_i_bwd_avg[i]
          if self.x_i_bwd_avg[i]<x_i_avg_bwd_min:
              x_i_avg_bwd_min=self.x_i_bwd_avg[i]
        
        self.E_fwd=x_i_avg_fwd_max-x_i_avg_fwd_min
        self.E_bwd=x_i_avg_bwd_max-x_i_avg_bwd_min

        x_i_avg_max=x_i_avg_fwd_max
        if x_i_avg_bwd_max>x_i_avg_max:
            x_i_avg_max=x_i_avg_bwd_max
        x_i_avg_min=x_i_avg_fwd_min
        if x_i_avg_bwd_min>x_i_avg_min:
            x_i_avg_min=x_i_avg_bwd_min
            
        self.E=x_i_avg_max-x_i_avg_min
        print("E_fwd="+ str(self.E_fwd))
        print("E_bwd="+ str(self.E_bwd))
        print("E="+ str(self.E))

    def calcM(self):
        x_i_avg_max=self.x_i_avg[1]
        x_i_avg_min=self.x_i_avg[1]

        for i in range(1,self.positions+1):
          #fwd
          if self.x_i_avg[i]>x_i_avg_max:
            x_i_avg_max=self.x_i_avg[i]
          if self.x_i_avg[i]<x_i_avg_min:
            x_i_avg_min=self.x_i_avg[i]

        self.M=x_i_avg_max-x_i_avg_min
        print("M="+ str(self.M))

    def calcA(self):
        term_max_fwd=self.x_i_fwd_avg[1]+2*self.s_i_fwd[1]
        term_min_fwd=self.x_i_fwd_avg[1]-2*self.s_i_fwd[1]
        term_max_bwd=self.x_i_bwd_avg[1]+2*self.s_i_bwd[1]
        term_min_bwd=self.x_i_bwd_avg[1]-2*self.s_i_bwd[1]

        for i in range(1,self.positions+1):
          #fwd
          term_temp_fwd_max=self.x_i_fwd_avg[1]+2*self.s_i_fwd[i]
          term_temp_fwd_min=self.x_i_fwd_avg[1]-2*self.s_i_fwd[i]
          if term_temp_fwd_max>term_max_fwd:
            term_max_fwd=term_temp_fwd_max
          if term_temp_fwd_min<term_min_fwd:
            term_min_fwd=term_temp_fwd_min
          #bwd
          term_temp_bwd_max=self.x_i_bwd_avg[1]+2*self.s_i_bwd[i]
          term_temp_bwd_min=self.x_i_bwd_avg[1]-2*self.s_i_bwd[i]
          if term_temp_bwd_max>term_max_bwd:
            term_max_bwd=term_temp_bwd_max
          if term_temp_bwd_min<term_min_bwd:
            term_min_bwd=term_temp_bwd_min
        
        self.A_fwd=term_max_fwd-term_min_fwd
        self.A_bwd=term_max_bwd-term_min_bwd

        term_max_max=term_max_fwd
        term_min_min=term_min_fwd
        if term_max_bwd>term_max_max:
            term_max_max=term_max_bwd
        if term_min_bwd<term_min_min:
            term_min_min=term_min_bwd
        self.A=term_max_max-term_min_min
        print("A_fwd=" + str(self.A_fwd))
        print("A_bwd=" + str(self.A_bwd))

        print("A=" + str(self.A))


def main():
   
  if len(sys.argv ) > 2  :  
      printOutHelp()
      sys.exit()

  if len(sys.argv)==2:
    fname=sys.argv[1]
    dataFile=open(fname,'r')

  if len(sys.argv)==3:
    fname=""
    dataFile=sys.stdin

  iso=ecmcISO230_2()

  for line in dataFile:
      iso.parseLine(line)
  iso.calcX()
  iso.calcB()
  iso.calcS()
  iso.calcR()
  iso.calcE()
  iso.calcM()
  iso.calcA()
   
if __name__ == "__main__":
  main()
