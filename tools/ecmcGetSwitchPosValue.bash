#!/bin/bash
# 
# This script finds the position of a switch engaging or disaengaging
#
# Arg 1 File (if only 6 args then File is stdin)                    
# Arg 2 Trigg PV filter             IOC_TEST:TestNumber
# Arg 3 Trigg PV value              1001
# Arg 4 Data PV filter              IOC_TEST:ec0-s4-EL7211-Enc-PosAct, IOC_TEST:Axis1-PosAct, IOC_TEST:ec0-s5-OptoILD2300_50mm-AI1
# Arg 5 Data line count before test 50 
# Arg 6 Switch PV filter            IOC_TEST:ec0-s2-EL1808-BI
# Arg 7 Switch PVvalue              0
#
# Example: 
# bash ecmcGetSwitchPosValue.bash IOC_TEST:TestNumber 1001 IOC_TEST:ec0-s4-EL7211-Enc-PosAct 50 IOC_TEST:ec0-s2-EL1808-BI 0
#
# Author: Anders Sandström, anders.sandstrom@esss.se
#

ARGOK=0
if [ "$#" -eq 6 ]; then
    # Data from stdin
    FILE="-"
    TRIGGPV=$1
    TRIGGVAL=$2
    DATAPV=$3
    DATACOUNT=$4
    SWITCHPV=$5
    SWITCHVAL=$6
    ARGOK=1
fi
if [ "$#" -eq 7 ]; then
    # Data from file
    FILE=$1
    TRIGGPV=$2
    TRIGGVAL=$3
    DATAPV=$4
    DATACOUNT=$5
    SWITCHPV=$6
    SWITCHVAL=$7
    ARGOK=1
fi

if [ "$ARGOK" -ne 1 ]; then
  echo "ecmcGetSwitchPosValue: Wrong arg count..."
  exit 1  
fi

DATAPVS="$DATAPV\|$SWITCHPV"
DATA=$(bash ecmcGetLinesBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPVS} ${DATACOUNT})
# Get one openloop counter value just before BI1 1/0
DATACOUNT="1" 
DATA=$(echo "$DATA" | bash ecmcGetDataBeforeTrigg.bash ${SWITCHPV} ${SWITCHVAL} ${DATAPV} ${DATACOUNT})
echo "$DATA"
