#!/bin/bash
# 
#  Plot data
#
# Arg 1 Data file   (input)
#
# Author: Anders Sandström, anders.sandstrom@esss.se

# Newline
nl='
'
if [ "$#" -ne 1 ]; then
   echo "main: Wrong arg count... Please specify input and output file."
   exit 1 
fi

FILE=$1

TRIGGPV="IOC_TEST:TestNumber"
TRIGGVAL="1001"
DATAPV="IOC_TEST:ec0-s4-EL7211-Enc-PosAct"
DATACOUNT="10"
DEC=4

echo "FILE      = ${FILE}"
echo "TRIGGPV   = ${TRIGGPV}"
echo "TRIGGVAL  = ${TRIGGVAL}"
echo "DATAPV    = ${DATAPV}"
echo "DATACOUNT = ${DATACOUNT}"

echo "####################################################################"
DATA=$(bash ecmcGetLinesBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
DATA=$(echo "${DATA}" | bash ecmcOffsetLines.bash 10.1)
echo "${DATA}"
echo "####################################################################"
DATA=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
DATA=$(echo "${DATA}" | bash ecmcOffsetData.bash 10.1)
echo "${DATA}"
AVG=$(echo "${DATA}" | bash ecmcAvgData.bash)
echo "AVG= ${AVG}" 
echo "####################################################################"
DATA=$(bash ecmcGetLinesBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
echo "${DATA}"
echo "####################################################################"

# Find resolver value at 35mm (on open loop counter).
TRIGGPV="IOC_TEST:TestNumber"
TRIGGVAL="3305"
DATAPV="IOC_TEST:ec0-s4-EL7211-Enc-PosAct"
DATACOUNT="50"
DATA=$(bash ecmcGetLinesBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
RESOLVER_VAL_AT_35=$(echo "${DATA}" | bash ecmcAvgLines.bash)
echo "Resolver val at 35mm                = ${RESOLVER_VAL_AT_35}"

# Find microepsilon optical sensor value at 35mm (on open loop counter).
TRIGGPV="IOC_TEST:TestNumber"
TRIGGVAL="3305"
DATAPV="IOC_TEST:ec0-s5-OptoILD2300_50mm-AI1"
DATACOUNT="1"  # Not updating every cycle
DATA=$(bash ecmcGetLinesBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
# Need to reverse sign since positive in negative ditrection
OPTO_VAL_AT_35=$(echo "${DATA}" | bash ecmcScaleLines.bash -1 | bash ecmcAvgLines.bash)
echo "Opto val at 35mm                    = ${OPTO_VAL_AT_35}"

# Find open loop sensor value at 35mm (on open loop counter) (should be very close 35, just to check!!).
TRIGGPV="IOC_TEST:TestNumber"
TRIGGVAL="3305"
DATAPV="IOC_TEST:Axis1-PosAct"
DATACOUNT="1" # Just one value since on change and open loop counter is not changing at standstill
DATA=$(bash ecmcGetLinesBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
# Need to reverse sign since positive in negative ditrection
OPEN_LOOP_VAL_AT_35=$(echo "${DATA}" | bash ecmcAvgLines.bash)
echo "Openloop val at 35mm                = ${OPEN_LOOP_VAL_AT_35}"

echo "This leads to the following offsets to open loop counter:"
# Calculate offsets for the sensors to get in same coord system (origo at 35mm open loop counter)
OPTO_OFFSET=$(awk -v sensor=${OPTO_VAL_AT_35} -v ref=${OPEN_LOOP_VAL_AT_35} "BEGIN {print ref-sensor}")
echo "Opto offset     = ${OPTO_OFFSET}"

# Calculate offsets for the sensors to get in same coord system (origo at 35mm open loop counter)
RESOLVER_OFFSET=$(awk -v sensor=${RESOLVER_VAL_AT_35} -v ref=${OPEN_LOOP_VAL_AT_35} "BEGIN {print ref-sensor}")
echo "Resolver offset = ${RESOLVER_OFFSET}"

## Start plot stuff!

TRIGGPV="IOC_TEST:TestNumber"
TRIGGVAL="6001"

DATAPV="IOC_TEST:ec0-s4-EL7211-Enc-PosAct"
DATACOUNT="7000"
RESOLVER=$(bash ecmcGetLinesBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
RESOLVER=$(echo "$RESOLVER" | bash ecmcScaleOffsetLines.bash 1 ${RESOLVER_OFFSET})
RESOLVER+=$nl

DATAPV="IOC_TEST:Axis1-PosAct"
DATACOUNT="8000"
OPEN=$(bash ecmcGetLinesBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
OPEN+=$nl

DATAPV="IOC_TEST:ec0-s5-OptoILD2300_50mm-AI1"
DATACOUNT="6000"
OPTO=$(bash ecmcGetLinesBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
OPTO=$(echo "$OPTO" | bash ecmcScaleOffsetLines.bash -1 ${OPTO_OFFSET})

echo  "${RESOLVER}" "${OPEN}" "${OPTO}" | python ../pyDataManip/plotCaMonitor.py
#echo "$RESOLVER" | python ../pyDataManip/plotCaMonitor.py
#echo "$OPTO" | python ../pyDataManip/plotCaMonitor.py
#echo "$OPEN" | python ../pyDataManip/plotCaMonitor.py
