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

# Example table
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

## Init report file
bash ecmcReportInit.bash $REPORT $FILE

## Write sensor information
bash ecmcReport.bash $REPORT "# Sensors"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "## Open loop step counter of stepper"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "The stepper motors was run in open loop during all the tests. The openloop step counter"
bash ecmcReport.bash $REPORT "reflects the actual position of the contolsystem."
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "## Resolver:"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Conversion data (to open loop coord syst):"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "1. Scale factor  : 1"
bash ecmcReport.bash $REPORT "2. Offset : ${RESOLVER_OFFSET}mm"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "## External verification system, Micro-Epsilon ILD2300 sensor"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Conversion data (to open loop coord syst):"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "1. Scale factor  : -1 (measure from top)"
bash ecmcReport.bash $REPORT "2. Offset : ${OPTO_OFFSET}mm"
bash ecmcReport.bash $REPORT ""

echo "####################################################################"

##### Switches ##########################################################
bash mainSwitch.bash $FILE $REPORT $RESOLVER_OFFSET $OPTO_OFFSET $DEC

##### Repeatability #####################################################
bash mainRepeatability.bash $FILE $REPORT $RESOLVER_OFFSET $OPTO_OFFSET $DEC

##### Resolver jitter ###################################################
bash mainResolverStandstill.bash $FILE $REPORT $RESOLVER_OFFSET $OPTO_OFFSET 5 1000

##### Accuracy FWD ######################################################
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "## Accuracy based on Resolver and ILD2300 Sensor Positive Direction"
bash mainAccuracy.bash $FILE $REPORT $RESOLVER_OFFSET $OPTO_OFFSET $DEC 8000 0

##### Accuracy BWD ######################################################
bash ecmcReport.bash $REPORT "## Accuracy based on Resolver and ILD2300 Sensor Negative Direction"
bash mainAccuracy.bash $FILE $REPORT $RESOLVER_OFFSET $OPTO_OFFSET $DEC 7000 1
