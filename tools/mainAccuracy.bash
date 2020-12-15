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
# Arg 7 Reverse
#
# Author: Anders Sandström, anders.sandstrom@esss.se
#

# Newline
nl='
'
if [ "$#" -ne 7 ]; then
   echo "mainResolverStandstill: Wrong arg count... Please specify input and output file."
   exit 1 
fi

FILE=$1
REPORT=$2
RESOLVER_OFFSET=$3
OPTO_OFFSET=$4
DEC=$5
TESTBASE=$6
REVERSE=$7

# Finds out what position by reading setpoint
DATACOUNT_RESOLVER="75"
TESTCOUNT=12

# Resolver 
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Measured at $TESTCOUNT positions offset by 5mm over the entire actuator stroke."
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Test | Setpoint [mm] | Resolver [mm] | Diff [mm] | ILD2300 [mm] | Diff [mm]"
bash ecmcReport.bash $REPORT "--- | --- | --- | --- | --- | --- |"

TRIGGPV="IOC_TEST:TestNumber"
DIFFS=""
DATACOUNT="1"

for COUNTER in {1..12}
do
   if [ "$REVERSE" -eq 0 ]; then
      let "TRIGGVAL=$TESTBASE+$COUNTER"
   else
      let "TRIGGVAL=$TESTBASE+13-$COUNTER"
   fi

   # setpoint   
   DATAPV="IOC_TEST:Axis1-PosSet"
   SETPOINT=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   echo "Setpoint=$SETPOINT"

   # resolver
   DATAPV="IOC_TEST:ec0-s4-EL7211-Enc-PosAct"   
   RESOLVER_VAL=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   RESOLVER_VAL=$(echo "$RESOLVER_VAL" | bash ecmcScaleOffsetLines.bash 1 ${RESOLVER_OFFSET})
   DIFF_RESOLVER=$(echo "$RESOLVER_VAL-$SETPOINT" | bc -l)
   DIFFS_RESOLVER+="$DIFF_RESOLVER "
   echo "Resolver value = $RESOLVER_VAL"
   
   # opto
   DATAPV="IOC_TEST:ec0-s5-OptoILD2300_50mm-AI1"
   OPTO_VAL=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   OPTO_VAL=$(echo $OPTO_VAL | bash ecmcScaleOffsetData.bash -1 ${OPTO_OFFSET})
   # Ensure ILD2300 value is valid (>0)
   if (( $(echo "$OPTO_VAL < 0.0" | bc -l) )); then
      OPTO_VAL="Out of range"
      DIFF_OPTO="NaN"
      printf "%d | %.${DEC}f | %.${DEC}f | %.${DEC}f | %s | %s\n" $COUNTER $SETPOINT $RESOLVER_VAL $DIFF_RESOLVER "$OPTO_VAL" "$DIFF_OPTO" >> $REPORT
   else   
      DIFF_OPTO=$(echo "$OPTO_VAL-$SETPOINT" | bc -l)
      DIFFS_OPTO+="$DIFF_OPTO "
      printf "%d | %.${DEC}f | %.${DEC}f | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $COUNTER $SETPOINT $RESOLVER_VAL $DIFF_RESOLVER $OPTO_VAL $DIFF_OPTO >> $REPORT
   fi
   
   echo "Opto value =$OPTO_VAL"
   
done
# Write max diffs
ACCURACY_RES_DIFF=$(echo "$DIFFS_RESOLVER" | bash ecmcAbsMaxDataRow.bash)
ACCURACY_OPTO_DIFF=$(echo "$DIFFS_OPTO" | bash ecmcAbsMaxDataRow.bash)

printf "Accuracy |-|-| %.${DEC}f | - | %.${DEC}f\n" $ACCURACY_RES_DIFF $ACCURACY_OPTO_DIFF  >> $REPORT

bash ecmcReport.bash $REPORT ""


printf "Accuracy (Resolver): %.${DEC}f\n" $ACCURACY_RES_DIFF >> $REPORT
printf "Accuracy (ILD2300): %.${DEC}f\n" $ACCURACY_OPTO_DIFF >> $REPORT
bash ecmcReport.bash $REPORT ""
