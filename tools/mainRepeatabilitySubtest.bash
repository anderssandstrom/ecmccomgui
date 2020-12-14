#!/bin/bash
# 
# Main script for processing data for bifrost slitset SAT.
#
# Arg 1 Data file   (input)
# Arg 2 Report file (output)
# Arg 3 Resolver offset
# Arg 4 Opto offset
# Arg 5 Decimals
# Arg 6 TestBase Pos
# Arg 7 TestBase Nos
#
# Author: Anders Sandström, anders.sandstrom@esss.se
#

# Newline
nl='
'
if [ "$#" -ne 7 ]; then
   echo "mainRepeatabilitySubtest: Wrong arg count... Please specify input and output file."
   exit 1 
fi

FILE=$1
REPORT=$2
RESOLVER_OFFSET=$3
OPTO_OFFSET=$4
DEC=$5
POS=$6
NEG=$7

# Finds out what position by reading setpoint

let "TRIGGVAL=$POS+1"
TRIGGPV="IOC_TEST:TestNumber"
DATACOUNT="1"
DATAPV="IOC_TEST:Axis1-PosSet"
SETPOINT=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
echo "Setpoint=$SETPOINT"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "## Target Position $SETPOINT Positive and Negative Direction"

TRIGGPV="IOC_TEST:TestNumber"
DATACOUNT="1"
RESOLVERVALS=""
OPTOVALS=""

# Open loop counter
#bash ecmcReport.bash $REPORT "Test | Openloop Pos [mm] | Openloop Neg [mm]"
#bash ecmcReport.bash $REPORT "--- | --- | --- |"
#DATAPV="IOC_TEST:Axis1-PosAct"
#for COUNTER in {1..10}
#do
#   # positive
#   let "TRIGGVAL=$COUNTER+3100"
#   OPENLOOPVALPOS=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
#   OPENLOOPVALSPOS+="$OPENLOOPVALPOS "
#   echo "Openloop value pos=$OPENLOOPVALPOS"
#   
#   # negative
#   let "TRIGGVAL=$COUNTER+3200"   
#   OPENLOOPVALNEG=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
#   OPENLOOPVALSNEG+="$OPENLOOPVALNEG "
#   echo "Openloop value neg=$OPENLOOPVALNEG"
#   
#   printf "%d | %.${DEC}f | %.${DEC}f\n" $COUNTER $OPENLOOPVALPOS $OPENLOOPVALNEG >> $REPORT
#done

# Resolver 
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Test | Resolver Pos [mm] | Resolver Neg [mm] | Diff [mm]"
bash ecmcReport.bash $REPORT "--- | --- | --- | --- |"
DATAPV="IOC_TEST:ec0-s4-EL7211-Enc-PosAct"
DIFFS=""
RESOLVER_VALS_NEG=""
RESOLVER_VALS_POS=""
OPTO_VALS_POS=""
OPTO_VALS_NEG=""

for COUNTER in {1..10}
do
   # positive
   let "TRIGGVAL=$COUNTER+$POS"
   RESOLVER_VAL_POS=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   RESOLVER_VAL_POS=$(echo $RESOLVER_VAL_POS | bash ecmcScaleOffsetData.bash 1 ${RESOLVER_OFFSET})
   RESOLVER_VALS_POS+="$RESOLVER_VAL_POS "
   echo "Resolver value pos=$RESOLVER_VAL_POS"

   # neg
   let "TRIGGVAL=$COUNTER+$NEG"
   RESOLVER_VAL_NEG=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   RESOLVER_VAL_NEG=$(echo $RESOLVER_VAL_NEG | bash ecmcScaleOffsetData.bash 1 ${RESOLVER_OFFSET})
   RESOLVER_VALS_NEG+="$RESOLVER_VAL_NEG "
   echo "Resolver value neg=$RESOLVER_VAL_NEG"
   DIFF=$(awk "BEGIN {print ($RESOLVER_VAL_POS-($RESOLVER_VAL_NEG))}")
   DIFFS+="$DIFF "

   printf "%d | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $COUNTER $RESOLVER_VAL_POS $RESOLVER_VAL_NEG $DIFF >> $REPORT

done

RESOLVER_AVG_POS=$(echo "$RESOLVER_VALS_POS" | bash ecmcAvgDataRow.bash)
RESOLVER_STD_POS=$(echo "$RESOLVER_VALS_POS" | bash ecmcStdDataRow.bash)
RESOLVER_AVG_NEG=$(echo "$RESOLVER_VALS_NEG" | bash ecmcAvgDataRow.bash)
RESOLVER_STD_NEG=$(echo "$RESOLVER_VALS_NEG" | bash ecmcStdDataRow.bash)
DIFF_AVG=$(awk "BEGIN {print ($RESOLVER_AVG_POS-($RESOLVER_AVG_NEG))}")
DIFF_STD=$(awk "BEGIN {print ($RESOLVER_STD_POS-($RESOLVER_STD_NEG))}")
echo "Resolver Pos AVG=$RESOLVER_AVG_POS, STD=$RESOLVER_STD_POS"
echo "Resolver Neg AVG=$RESOLVER_AVG_NEG, STD=$RESOLVER_STD_NEG"
printf "AVG | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $RESOLVER_AVG_POS $RESOLVER_AVG_NEG $DIFF_AVG >> $REPORT
printf "STD | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $RESOLVER_STD_POS $RESOLVER_STD_NEG $DIFF_STD >> $REPORT

# Opto
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Test | Opto Pos [mm] | Opto Neg [mm] | Diff [mm]"
bash ecmcReport.bash $REPORT "--- | --- | --- | --- |"
DATAPV="IOC_TEST:ec0-s5-OptoILD2300_50mm-AI1"
DIFFS=""
RESOLVER_VALS_NEG=""
RESOLVER_VALS_POS=""
OPTO_VALS_POS=""
OPTO_VALS_NEG=""
for COUNTER in {1..10}
do
   # positive
   let "TRIGGVAL=$COUNTER+$POS"
   OPTO_VAL_POS=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   OPTO_VAL_POS=$(echo $OPTO_VAL_POS | bash ecmcScaleOffsetData.bash -1 ${OPTO_OFFSET})
   OPTO_VALS_POS+="$OPTO_VAL_POS "
   echo "Opto value pos =$OPTO_VAL_POS"

   # negative
   let "TRIGGVAL=$COUNTER+$NEG"
   OPTO_VAL_NEG=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   OPTO_VAL_NEG=$(echo $OPTO_VAL_NEG | bash ecmcScaleOffsetData.bash -1 ${OPTO_OFFSET})
   OPTO_VALS_NEG+="$OPTO_VAL_NEG "
   echo "Opto value neg=$OPTO_VAL_NEG"
   DIFF=$(awk "BEGIN {print ($OPTO_VAL_POS-($OPTO_VAL_NEG))}")
   DIFFS+="$DIFF "
   printf "%d | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $COUNTER $OPTO_VAL_POS $OPTO_VAL_NEG $DIFF >> $REPORT
done

OPTO_AVG_POS=$(echo "$OPTO_VALS_POS" | bash ecmcAvgDataRow.bash)
OPTO_STD_POS=$(echo "$OPTO_VALS_POS" | bash ecmcStdDataRow.bash)
OPTO_AVG_NEG=$(echo "$OPTO_VALS_NEG" | bash ecmcAvgDataRow.bash)
OPTO_STD_NEG=$(echo "$OPTO_VALS_NEG" | bash ecmcStdDataRow.bash)
DIFF_AVG=$(awk "BEGIN {print ($OPTO_AVG_POS-($OPTO_AVG_NEG))}")
DIFF_STD=$(awk "BEGIN {print ($OPTO_STD_POS-($OPTO_STD_NEG))}")
echo "OPTO POS AVG=$OPTO_AVG_POS, STD=$OPTO_STD_POS"
echo "OPTO NEG AVG=$OPTO_AVG_NEG, STD=$OPTO_STD_NEG"
printf "AVG | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $OPTO_AVG_POS $OPTO_AVG_NEG $DIFF_AVG>> $REPORT
printf "STD | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $OPTO_STD_POS $OPTO_STD_NEG $DIFF_STD>> $REPORT
