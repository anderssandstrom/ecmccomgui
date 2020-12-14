#!/bin/bash
# 
# Main script for processing data for bifrost slitset SAT.
#
# Arg 1 Data file   (input)
# Arg 2 Report file (output)
# Arg 3 Resolver offset
# Arg 4 Opto offset
# Arg 5 Decimals
#
# Author: Anders Sandström, anders.sandstrom@esss.se
#

# Newline
nl='
'
if [ "$#" -ne 5 ]; then
   echo "mainRepeatability: Wrong arg count... Please specify input and output file."
   exit 1 
fi

FILE=$1
REPORT=$2
RESOLVER_OFFSET=$3
OPTO_OFFSET=$4
DEC=$5

bash ecmcReport.bash $REPORT "# Repeatability"
bash ecmcReport.bash $REPORT ""

############## Pos 15 POS
TRIGGVAL=3101
TRIGGPV="IOC_TEST:TestNumber"
DATACOUNT="1"
DATAPV="IOC_TEST:Axis1-PosSet"
SETPOINT=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
echo "Setpoint=$SETPOINT"

bash ecmcReport.bash $REPORT "## Target Position $SETPOINT Positive and Negative Direction"
bash ecmcReport.bash $REPORT ""

TRIGGPV="IOC_TEST:TestNumber"
DATACOUNT="1"
RESOLVERVALS=""
OPENLOOPVALS=""
OPTOVALS=""

# Open loop counter
bash ecmcReport.bash $REPORT "Test | Openloop Pos [mm] | Openloop Neg [mm]"
bash ecmcReport.bash $REPORT "--- | --- | --- |"
DATAPV="IOC_TEST:Axis1-PosAct"
for COUNTER in {1..10}
do
   # positive
   let "TRIGGVAL=$COUNTER+3100"
   OPENLOOPVALPOS=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   OPENLOOPVALSPOS+="$OPENLOOPVALPOS "
   echo "Openloop value pos=$OPENLOOPVALPOS"
   
   # negative
   let "TRIGGVAL=$COUNTER+3200"   
   OPENLOOPVALNEG=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   OPENLOOPVALSNEG+="$OPENLOOPVALNEG "
   echo "Openloop value neg=$OPENLOOPVALNEG"
   
   printf "%d | %.${DEC}f | %.${DEC}f\n" $COUNTER $OPENLOOPVALPOS $OPENLOOPVALNEG >> $REPORT
done

# Resolver 
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Test | Resolver Pos [mm] | Resolver Neg [mm]"
bash ecmcReport.bash $REPORT "--- | --- | --- |"
DATAPV="IOC_TEST:ec0-s4-EL7211-Enc-PosAct"
for COUNTER in {1..10}
do
   # positive
   let "TRIGGVAL=$COUNTER+3100"
   RESOLVERVALPOS=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   RESOLVERVALPOS=$(echo $RESOLVERVALPOS | bash ecmcScaleOffsetData.bash 1 ${RESOLVER_OFFSET})
   RESOLVERVALSPOS+="$RESOLVERVALPOS "
   echo "Resolver value pos=$RESOLVERVALPOS"

   # neg
   let "TRIGGVAL=$COUNTER+3200"
   RESOLVERVALNEG=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   RESOLVERVALNEG=$(echo $RESOLVERVALNEG | bash ecmcScaleOffsetData.bash 1 ${RESOLVER_OFFSET})
   RESOLVERVALSNEG+="$RESOLVERVALNEG "
   echo "Resolver value neg=$RESOLVERVALNEG"

   printf "%d | %.${DEC}f | %.${DEC}f\n" $COUNTER $RESOLVERVALPOS $RESOLVERVALNEG >> $REPORT
done

# Opto
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Test | Opto Pos [mm] | Opto Neg [mm]"
bash ecmcReport.bash $REPORT "--- | --- | --- |"
DATAPV="IOC_TEST:ec0-s5-OptoILD2300_50mm-AI1"
for COUNTER in {1..10}
do
   # positive
   let "TRIGGVAL=$COUNTER+3100"
   OPTOVALPOS=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   OPTOVALPOS=$(echo $OPTOVALPOS | bash ecmcScaleOffsetData.bash -1 ${OPTO_OFFSET})
   OPTOVALSPOS+="$OPTOVALPOS "
   echo "Opto value pos =$OPTOVALPOS"

   # negative
   let "TRIGGVAL=$COUNTER+3200"
   OPTOVALNEG=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   OPTOVALNEG=$(echo $OPTOVALNEG | bash ecmcScaleOffsetData.bash -1 ${OPTO_OFFSET})
   OPTOVALSNEG+="$OPTOVALNEG "
   echo "Opto value neg=$OPTOVALNEG"

   printf "%d | %.${DEC}f | %.${DEC}f\n" $COUNTER $OPTOVALPOS $OPTOVALNEG >> $REPORT
done


############## Pos 35 POS
TRIGGVAL=3301
TRIGGPV="IOC_TEST:TestNumber"
DATACOUNT="1"
DATAPV="IOC_TEST:Axis1-PosSet"
SETPOINT=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
echo "Setpoint=$SETPOINT"

bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "## Target Position $SETPOINT Positive and Negative Direction"
bash ecmcReport.bash $REPORT ""

TRIGGPV="IOC_TEST:TestNumber"
DATACOUNT="1"
RESOLVERVALS=""
OPENLOOPVALS=""
OPTOVALS=""

# Open loop counter
bash ecmcReport.bash $REPORT "Test | Openloop Pos [mm] | Openloop Neg [mm]"
bash ecmcReport.bash $REPORT "--- | --- | --- |"
DATAPV="IOC_TEST:Axis1-PosAct"
for COUNTER in {1..10}
do
   # positive
   let "TRIGGVAL=$COUNTER+3300"
   OPENLOOPVALPOS=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   OPENLOOPVALSPOS+="$OPENLOOPVALPOS "
   echo "Openloop value pos=$OPENLOOPVALPOS"
   
   # negative
   let "TRIGGVAL=$COUNTER+3400"   
   OPENLOOPVALNEG=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   OPENLOOPVALSNEG+="$OPENLOOPVALNEG "
   echo "Openloop value neg=$OPENLOOPVALNEG"
   
   printf "%d | %.${DEC}f | %.${DEC}f\n" $COUNTER $OPENLOOPVALPOS $OPENLOOPVALNEG >> $REPORT
done

# Resolver 
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Test | Resolver Pos [mm] | Resolver Neg [mm]"
bash ecmcReport.bash $REPORT "--- | --- | --- |"
DATAPV="IOC_TEST:ec0-s4-EL7211-Enc-PosAct"
for COUNTER in {1..10}
do
   # positive
   let "TRIGGVAL=$COUNTER+3300"
   RESOLVERVALPOS=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   RESOLVERVALPOS=$(echo $RESOLVERVALPOS | bash ecmcScaleOffsetData.bash 1 ${RESOLVER_OFFSET})
   RESOLVERVALSPOS+="$RESOLVERVALPOS "
   echo "Resolver value pos=$RESOLVERVALPOS"

   # neg
   let "TRIGGVAL=$COUNTER+3400"
   RESOLVERVALNEG=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   RESOLVERVALNEG=$(echo $RESOLVERVALNEG | bash ecmcScaleOffsetData.bash 1 ${RESOLVER_OFFSET})
   RESOLVERVALSNEG+="$RESOLVERVALNEG "
   echo "Resolver value neg=$RESOLVERVALNEG"

   printf "%d | %.${DEC}f | %.${DEC}f\n" $COUNTER $RESOLVERVALPOS $RESOLVERVALNEG >> $REPORT
done

# Opto
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Test | Opto Pos [mm] | Opto Neg [mm]"
bash ecmcReport.bash $REPORT "--- | --- | --- |"
DATAPV="IOC_TEST:ec0-s5-OptoILD2300_50mm-AI1"
for COUNTER in {1..10}
do
   # positive
   let "TRIGGVAL=$COUNTER+3300"
   OPTOVALPOS=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   OPTOVALPOS=$(echo $OPTOVALPOS | bash ecmcScaleOffsetData.bash -1 ${OPTO_OFFSET})
   OPTOVALSPOS+="$OPTOVALPOS "
   echo "Opto value pos =$OPTOVALPOS"

   # negative
   let "TRIGGVAL=$COUNTER+3400"
   OPTOVALNEG=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   OPTOVALNEG=$(echo $OPTOVALNEG | bash ecmcScaleOffsetData.bash -1 ${OPTO_OFFSET})
   OPTOVALSNEG+="$OPTOVALNEG "
   echo "Opto value neg=$OPTOVALNEG"

   printf "%d | %.${DEC}f | %.${DEC}f\n" $COUNTER $OPTOVALPOS $OPTOVALNEG >> $REPORT
done

############## Pos 55 POS
TRIGGVAL=3501
TRIGGPV="IOC_TEST:TestNumber"
DATACOUNT="1"
DATAPV="IOC_TEST:Axis1-PosSet"
SETPOINT=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
echo "Setpoint=$SETPOINT"

bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "## Target Position $SETPOINT Positive and Negative Direction"
bash ecmcReport.bash $REPORT ""

TRIGGPV="IOC_TEST:TestNumber"
DATACOUNT="1"
RESOLVERVALS=""
OPENLOOPVALS=""
OPTOVALS=""

# Open loop counter
bash ecmcReport.bash $REPORT "Test | Openloop Pos [mm] | Openloop Neg [mm]"
bash ecmcReport.bash $REPORT "--- | --- | --- |"
DATAPV="IOC_TEST:Axis1-PosAct"
for COUNTER in {1..10}
do
   # positive
   let "TRIGGVAL=$COUNTER+3500"
   OPENLOOPVALPOS=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   OPENLOOPVALSPOS+="$OPENLOOPVALPOS "
   echo "Openloop value pos=$OPENLOOPVALPOS"
   
   # negative
   let "TRIGGVAL=$COUNTER+3600"   
   OPENLOOPVALNEG=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   OPENLOOPVALSNEG+="$OPENLOOPVALNEG "
   echo "Openloop value neg=$OPENLOOPVALNEG"
   
   printf "%d | %.${DEC}f | %.${DEC}f\n" $COUNTER $OPENLOOPVALPOS $OPENLOOPVALNEG >> $REPORT
done

# Resolver 
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Test | Resolver Pos [mm] | Resolver Neg [mm]"
bash ecmcReport.bash $REPORT "--- | --- | --- |"
DATAPV="IOC_TEST:ec0-s4-EL7211-Enc-PosAct"
for COUNTER in {1..10}
do
   # positive
   let "TRIGGVAL=$COUNTER+3500"
   RESOLVERVALPOS=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   RESOLVERVALPOS=$(echo $RESOLVERVALPOS | bash ecmcScaleOffsetData.bash 1 ${RESOLVER_OFFSET})
   RESOLVERVALSPOS+="$RESOLVERVALPOS "
   echo "Resolver value pos=$RESOLVERVALPOS"

   # neg
   let "TRIGGVAL=$COUNTER+3600"
   RESOLVERVALNEG=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   RESOLVERVALNEG=$(echo $RESOLVERVALNEG | bash ecmcScaleOffsetData.bash 1 ${RESOLVER_OFFSET})
   RESOLVERVALSNEG+="$RESOLVERVALNEG "
   echo "Resolver value neg=$RESOLVERVALNEG"

   printf "%d | %.${DEC}f | %.${DEC}f\n" $COUNTER $RESOLVERVALPOS $RESOLVERVALNEG >> $REPORT
done

# Opto
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Test | Opto Pos [mm] | Opto Neg [mm]"
bash ecmcReport.bash $REPORT "--- | --- | --- |"
DATAPV="IOC_TEST:ec0-s5-OptoILD2300_50mm-AI1"
for COUNTER in {1..10}
do
   # positive
   let "TRIGGVAL=$COUNTER+3500"
   OPTOVALPOS=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   OPTOVALPOS=$(echo $OPTOVALPOS | bash ecmcScaleOffsetData.bash -1 ${OPTO_OFFSET})
   OPTOVALSPOS+="$OPTOVALPOS "
   echo "Opto value pos =$OPTOVALPOS"

   # negative
   let "TRIGGVAL=$COUNTER+3600"
   OPTOVALNEG=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   OPTOVALNEG=$(echo $OPTOVALNEG | bash ecmcScaleOffsetData.bash -1 ${OPTO_OFFSET})
   OPTOVALSNEG+="$OPTOVALNEG "
   echo "Opto value neg=$OPTOVALNEG"

   printf "%d | %.${DEC}f | %.${DEC}f\n" $COUNTER $OPTOVALPOS $OPTOVALNEG >> $REPORT
done

bash ecmcReport.bash $REPORT ""

