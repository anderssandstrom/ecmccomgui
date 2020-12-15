#!/bin/bash
# 
# Main script for processing data for bifrost slitset SAT.
#
# Arg 1 Data file   (input)
# Arg 2 Report file (output)
# Arg 3 Resolver offset
# Arg 4 Opto offset
# Arg 5 Decimals
# Arg 6 TestBase
#
# Author: Anders Sandström, anders.sandstrom@esss.se
#

# Newline
nl='
'
if [ "$#" -ne 6 ]; then
   echo "mainResolverStandstill: Wrong arg count... Please specify input and output file."
   exit 1 
fi

FILE=$1
REPORT=$2
RESOLVER_OFFSET=$3
OPTO_OFFSET=$4
DEC=$5
TESTBASE=$6


# Finds out what position by reading setpoint


bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "## Resolver Jitter at ${SETPOINT}mm setpoint"

# Resolver 
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Test | Setpoint [mm] | Resolver AVG[mm] | Resolver STD[mm]"
bash ecmcReport.bash $REPORT "--- | --- | --- | --- |"

TRIGGPV="IOC_TEST:TestNumber"
DIFFS=""

for COUNTER in {1..8}
do
   # setpoint
   DATACOUNT="1"
   let "TRIGGVAL=$TESTBASE+$COUNTER"

   DATAPV="IOC_TEST:Axis1-PosSet"
   SETPOINT=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   echo "Setpoint=$SETPOINT"

   # resolver
   DATAPV="IOC_TEST:ec0-s4-EL7211-Enc-PosAct"
   DATACOUNT="50"
   RESOLVER_VAL=$(bash ecmcGetLinesBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   RESOLVER_VAL=$(echo "$RESOLVER_VAL" | bash ecmcScaleOffsetLines.bash 1 ${RESOLVER_OFFSET})
   RESOLVER_AVG=$(echo "$RESOLVER_VAL" | bash ecmcAvgLines.bash)
   RESOLVER_STD=$(echo "$RESOLVER_VAL" | bash ecmcStdLines.bash)

   echo "Resolver value AVG = $RESOLVER_AVG STD = $RESOLVER_STD"
   
   printf "%d | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $COUNTER $SETPOINT $RESOLVER_AVG $RESOLVER_STD >> $REPORT
   echo "DATA=$RESOLVER_VAL"
   echo "$RESOLVER_VAL" | python ../pyDataManip/histCaMonitor.py
done
