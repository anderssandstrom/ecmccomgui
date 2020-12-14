#!/bin/bash
# 
# Main script for processing data for bifrost slitset SAT.
#
# Arg 1 Data file   (input)
# Arg 2 Report file (output)
#
# Author: Anders Sandström, anders.sandstrom@esss.se
#
# Data examples:
# IOC_TEST:Axis1-PosAct          2020-12-11 12:47:59.380804 10.00078125  
# IOC_TEST:TestNumber 2020-12-11 12:57:31.157767 4008
# IOC_TEST:ec0-s4-EL7211-Enc-PosAct 2020-12-11 12:45:50.390806 -12.14605904  
# IOC_TEST:Axis1-PosSet          2020-12-11 12:45:50.390806 0.053556875  
# IOC_TEST:ec0-s5-OptoILD2300_50mm-AI1 2020-12-11 12:47:59.400804 50.498368  
# IOC_TEST:ec0-s2-EL1808-BI1     2020-12-11 12:44:37.040810 1  
# IOC_TEST:ec0-s2-EL1808-BI2     2020-12-11 12:11:08.720807 1  
#
# Markdown to PDF notes
# 1: https://www.markdowntopdf.com
# 2: 
# pip install grip  
# grip your_markdown.md
# grip will render the markdown on localhost:5000 or similar (ex: go to http://localhost:5000/) - just edit away and refresh the browser. Print when ready.

# Newline
nl='
'
if [ "$#" -ne 2 ]; then
   echo "main: Wrong arg count... Please specify input and output file."
   exit 1 
fi

FILE=$1
REPORT=$2
TRIGGPV="IOC_TEST:TestNumber"
TRIGGVAL="1001"
DATAPV="IOC_TEST:ec0-s4-EL7211-Enc-PosAct"
DATACOUNT="10"

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
DATACOUNT="30"  # Not updating every cycle
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

## Init report file
bash ecmcReportInit.bash $REPORT $FILE

## Write sensor information
bash ecmcReport.bash $REPORT "# Sensor calibration"
bash ecmcReport.bash $REPORT "Test were performed with three position feedback systems:"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "1: Open loop counter of stepper (used for control)"
bash ecmcReport.bash $REPORT "2: Resolver (included in the slitsets)"
bash ecmcReport.bash $REPORT "3: Laser triangulation sensor (external verification system)"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "## Open loop step counter of stepper"
bash ecmcReport.bash $REPORT "The stepper motors was run in open loop during all the tests. The openloop step counter"
bash ecmcReport.bash $REPORT "reflects the actual position of the ecmc contolsystem."
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "## Resolver:"
bash ecmcReport.bash $REPORT "Conversion data (to open loop coord syst):"
bash ecmcReport.bash $REPORT "1. Scale factor  : 1"
bash ecmcReport.bash $REPORT "2. Offset factor : ${RESOLVER_OFFSET}mm"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "## External verification system"
bash ecmcReport.bash $REPORT "Micro-Epsilon ILD2300 sensor:"
bash ecmcReport.bash $REPORT "1. Type          : Laser triangulation"
bash ecmcReport.bash $REPORT "2. Range         : 50mm (mounted to cover the center of the slitset stroke)"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Conversion data (to open loop coord syst):"
bash ecmcReport.bash $REPORT "1. Scale factor  : -1 (measure from top)"
bash ecmcReport.bash $REPORT "2. Offset factor : ${OPTO_OFFSET}mm"
bash ecmcReport.bash $REPORT ""

############ LOW LIMIT SWITCH
# Check Low limit switch accuracy
# IOC_TEST:Axis1-PosAct          s2020-12-11 12:47:59.380804 10.00078125  
# IOC_TEST:TestNumber 2020-12-11 12:57:31.157767 4008
# IOC_TEST:ec0-s4-EL7211-Enc-PosAct 2020-12-11 12:45:50.390806 -12.14605904  
# IOC_TEST:Axis1-PosSet          2020-12-11 12:45:50.390806 0.053556875  
# IOC_TEST:ec0-s5-OptoILD2300_50mm-AI1 2020-12-11 12:47:59.400804 50.498368  
# IOC_TEST:ec0-s2-EL1808-BI1     2020-12-11 12:44:37.040810 1  
# IOC_TEST:ec0-s2-EL1808-BI2     2020-12-11 12:11:08.720807 1  
#Test | Openloop [mm]| Resolver [mm]| 
#--- | --- | --- |
#1  |  0.0010 | -0.4760
#2  |  0.0010 | -0.4765
#3  |  0.0015 | -0.4770
#4  |  0.0020 | -0.4780
#5  |  0.005  | -0.4785
#6  |  -0.001 | -0.4790
#7  |  0.000  | -0.4795
#8  |  0.0015 | -0.4800
#9  |  0.005  | -0.4805
#10 |  -0.001 | -0.4815

bash ecmcReport.bash $REPORT "# Limit Switch Performance"
bash ecmcReport.bash $REPORT "## Low Limit Engage Position "
bash ecmcReport.bash $REPORT "Test | Openloop [mm]| Resolver [mm]|"
bash ecmcReport.bash $REPORT "--- | --- | --- |"

# Get one openloop counter value just before BI1 0
TRIGGPV="IOC_TEST:TestNumber"
TRIGGVAL="2001"
DATAPV="IOC_TEST:Axis1-PosAct"
DATACOUNT="350"  # Must be enough to capture the switch transition
SWITCHPV="IOC_TEST:ec0-s2-EL1808-BI1"
SWITCHVAL=0
OPENLOOPVALS=""
RESOLVERVALS=""
COUNTER=0
# Engage
for TRIGGVAL in {2001..2010}
do
   let "COUNTER=$COUNTER+1"
   DATAPV="IOC_TEST:Axis1-PosAct"
   OPENLOOPVAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   OPENLOOPVALS+="$OPENLOOPVAL "
   DATAPV="IOC_TEST:ec0-s4-EL7211-Enc-PosAct"
   RESOLVERVAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   RESOLVERVAL=$(echo $RESOLVERVAL | bash ecmcScaleOffsetData.bash 1 ${RESOLVER_OFFSET})
   RESOLVERVALS+="$RESOLVERVAL "
   echo "BWD switch engage position $TRIGGVAL: $OPENLOOPVAL, $RESOLVERVAL"
   printf "%d | %.4f | %.4f\n" $COUNTER $OPENLOOPVAL $RESOLVERVAL >> $REPORT
done
# Calc avg and std
OPENLOOPAVG=$(echo "$OPENLOOPVALS" | bash ecmcAvgDataRow.bash)
OPENLOOPSTD=$(echo "$OPENLOOPVALS" | bash ecmcStdDataRow.bash)
echo "Openloop AVG=$OPENLOOPAVG, STD=$OPENLOOPSTD" 
RESOLVERAVG=$(echo "$RESOLVERVALS" | bash ecmcAvgDataRow.bash)
RESOLVERSTD=$(echo "$RESOLVERVALS" | bash ecmcStdDataRow.bash)
echo "Resolver AVG=$RESOLVERAVG, STD=$RESOLVERSTD"
printf "AVG | %.4f | %.4f\n" $OPENLOOPAVG $RESOLVERAVG >> $REPORT
printf "STD | %.4f | %.4f\n" $OPENLOOPSTD $RESOLVERSTD >> $REPORT

# Disengage
SWITCHVAL=1
OPENLOOPVALS=""
RESOLVERVALS=""
OPENLOOPAVG=""
RESOLVERAVG=""
for TRIGGVAL in {2011..2020}
do
   DATAPV="IOC_TEST:Axis1-PosAct"
   OPENLOOPVAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   OPENLOOPVALS+="$OPENLOOPVAL "
   DATAPV="IOC_TEST:ec0-s4-EL7211-Enc-PosAct"
   RESOLVERVAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   RESOLVERVAL=$(echo $RESOLVERVAL | bash ecmcScaleOffsetData.bash 1 ${RESOLVER_OFFSET})
   RESOLVERVALS+="$RESOLVERVAL "
   echo "BWD switch disengage position $TRIGGVAL: $OPENLOOPVAL, $RESOLVERVAL"
done

# Calc avg and std
OPENLOOPAVG=$(echo "$OPENLOOPVALS" | bash ecmcAvgDataRow.bash)
OPENLOOPSTD=$(echo "$OPENLOOPVALS" | bash ecmcStdDataRow.bash)
echo "Openloop AVG=$OPENLOOPAVG, STD=$OPENLOOPSTD" 
RESOLVERAVG=$(echo "$RESOLVERVALS" | bash ecmcAvgDataRow.bash)
RESOLVERSTD=$(echo "$RESOLVERVALS" | bash ecmcStdDataRow.bash)
echo "Resolver AVG=$RESOLVERAVG, STD=$RESOLVERSTD"

############ HIGH LIMIT SWITCH
SWITCHPV="IOC_TEST:ec0-s2-EL1808-BI2"
SWITCHVAL=0
RESOLVERVALS=""
OPENLOOPVALS=""
OPENLOOPAVG=""
RESOLVERAVG=""
# Engage
for TRIGGVAL in {4001..4010}
do
   DATAPV="IOC_TEST:Axis1-PosAct"
   OPENLOOPVAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   OPENLOOPVALS+="$OPENLOOPVAL "
   DATAPV="IOC_TEST:ec0-s4-EL7211-Enc-PosAct"
   RESOLVERVAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   RESOLVERVAL=$(echo $RESOLVERVAL | bash ecmcScaleOffsetData.bash 1 ${RESOLVER_OFFSET})
   RESOLVERVALS+="$RESOLVERVAL "
   echo "FWD switch engage position $TRIGGVAL: $OPENLOOPVAL, $RESOLVERVAL"
done

# Calc avg and std
OPENLOOPAVG=$(echo "$OPENLOOPVALS" | bash ecmcAvgDataRow.bash)
OPENLOOPSTD=$(echo "$OPENLOOPVALS" | bash ecmcStdDataRow.bash)
echo "Openloop AVG=$OPENLOOPAVG, STD=$OPENLOOPSTD" 
RESOLVERAVG=$(echo "$RESOLVERVALS" | bash ecmcAvgDataRow.bash)
RESOLVERSTD=$(echo "$RESOLVERVALS" | bash ecmcStdDataRow.bash)
echo "Resolver AVG=$RESOLVERAVG, STD=$RESOLVERSTD"

# Disengage
SWITCHVAL=1
RESOLVERVALS=""
OPENLOOPVALS=""
OPENLOOPAVG=""
RESOLVERAVG=""
for TRIGGVAL in {4011..4020}
do
   DATAPV="IOC_TEST:Axis1-PosAct"
   OPENLOOPVAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   OPENLOOPVALS+="$OPENLOOPVAL "
   DATAPV="IOC_TEST:ec0-s4-EL7211-Enc-PosAct"
   RESOLVERVAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   RESOLVERVAL=$(echo $RESOLVERVAL | bash ecmcScaleOffsetData.bash 1 ${RESOLVER_OFFSET})
   RESOLVERVALS+="$RESOLVERVAL "
   echo "FWD switch disengage position $TRIGGVAL: $OPENLOOPVAL, $RESOLVERVAL"
done

# Calc avg and std
OPENLOOPAVG=$(echo "$OPENLOOPVALS" | bash ecmcAvgDataRow.bash)
OPENLOOPSTD=$(echo "$OPENLOOPVALS" | bash ecmcStdDataRow.bash)
echo "Openloop AVG=$OPENLOOPAVG, STD=$OPENLOOPSTD" 
RESOLVERAVG=$(echo "$RESOLVERVALS" | bash ecmcAvgDataRow.bash)
RESOLVERSTD=$(echo "$RESOLVERVALS" | bash ecmcStdDataRow.bash)
echo "Resolver AVG=$RESOLVERAVG, STD=$RESOLVERSTD"

############ REPEATABILITY

