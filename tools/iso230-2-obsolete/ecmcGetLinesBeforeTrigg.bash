#!/bin/bash
# 
# This script finds the trigg pv with teh corerct value and returns a certain count of datalines before the trigger according to a filter.
#
# Arg 1 File (if only 4 args then File is stdin)                    
# Arg 2 Trigg PV filter             IOC_TEST:TestNumber
# Arg 3 Trigg PV value              1001
# Arg 4 Data PV filter              IOC_TEST:ec0-s4-EL7211-Enc-PosAct, IOC_TEST:Axis1-PosAct, IOC_TEST:ec0-s5-OptoILD2300_50mm-AI1
# Arg 5 Data line count before test 50 
#
# Example: Return 50 lines of EL7211 data just before test 1100 flag is set
# bash ecmcGetLinesBeforeTest.bash axis2_data.log IOC_TEST:TestNumber 10 IOC_TEST:ec0-s4-EL7211-Enc-PosAct 50
#
# Author: Anders Sandström, anders.sandstrom@esss.se
#

ARGOK=0
if [ "$#" -eq 4 ]; then
    # Data from stdin
    FILE="-"
    TRIGGPV=$1
    TRIGGVAL=$2
    DATAPV=$3
    LINECOUNT=$4
    ARGOK=1
fi
if [ "$#" -eq 5 ]; then
    # Data from file
    FILE=$1
    TRIGGPV=$2
    TRIGGVAL=$3
    DATAPV=$4
    LINECOUNT=$5
    ARGOK=1
fi

if [ "$ARGOK" -ne 1 ]; then
  echo "ecmcGetLinesBeforeTrigg: Wrong arg count..."
  exit 1  
fi

#echo "FILE      = ${FILE}"
#echo "TRIGGPV   = ${TRIGGPV}"
#echo "TRIGGVAL  = ${TRIGGVAL}"
#echo "DATAPV    = ${DATAPV}"
#echo "LINECOUNT = ${LINECOUNT}"

# IOC_TEST:Axis1-PosAct          2020-12-11 12:47:59.380804 10.00078125  
# IOC_TEST:TestNumber 2020-12-11 12:57:31.157767 4008

#                    grep TRIGGPV or DATAPV         trim spaces           grep 50 rows before: "TRIGGPV"*" TRIGGVAL"        remove last line                        

# DATA=$(cat ${FILE} | grep "${TRIGGPV}\|${DATAPV}")
# echo "1: ${DATA}"
# DATA=$(echo "$DATA " | awk '{$1=$1;print}')
# echo "2: ${DATA}"
# DATA=$(echo "$DATA " | grep -B${LINECOUNT} "${TRIGGPV}.* ${TRIGGVAL}")
# echo "3: ${DATA}"
# DATA=$(echo "$DATA " | head -n -1)
# echo "4: ${DATA}"


DATA=$(cat ${FILE} | grep "${TRIGGPV}\|${DATAPV}" | awk '{$1=$1;print}' | grep -B${LINECOUNT} "${TRIGGPV}.* ${TRIGGVAL}" | head -n -1)
echo "${DATA}"
