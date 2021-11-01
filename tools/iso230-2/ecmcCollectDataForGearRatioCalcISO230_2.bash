#!/bin/bash
# 
# Arg 1 Data file   (input)
# Arg 2 Cycle count
# Arg 3 Test count

FILE=$1
CYCLE_COUNT=$2
TEST_COUNT=$3

nl='
'

TESTS=$(seq -w 1 1 $TEST_COUNT)
CYCLES=$(seq -w 1 1 $CYCLE_COUNT)

### Need to update these fileds for every FAT sat so everything is correct
##PV names:
MOTORACTPV="IOC_TEST:Axis1-PosAct"
MOTORSETPV="IOC_TEST:Axis1-PosSet"
RESOLVERPV="IOC_TEST:m0s004-Enc01-PosAct"
REFERENCEPV="IOC_TEST:m0s005-Enc01-PosAct"
TESTNUMPV="IOC_TEST:TestNumber"
TESTNUMBER_BASE=1
#Output data
LINES=""

# Forward tests
for CYCLE in $CYCLES;
do
  
  for TEST in $TESTS
  do   
   
   TESTNUMBER=$TESTNUMBER_BASE$CYCLE"0"$TEST
   
   # Target position
   DATAPV=$MOTORSETPV
   TRIGGPV=$TESTNUMPV
   TRIGGVAL=$TESTNUMBER
   DATACOUNT=1
   DATA=$(bash ecmcGetLinesBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT}) 
   LINES="$LINES $nl $DATA"

   # Open loop counter
   DATAPV=$MOTORACTPV
   TRIGGPV=$TESTNUMPV
   TRIGGVAL=$TESTNUMBER
   DATACOUNT=1
   DATA=$(bash ecmcGetLinesBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})   
   LINES="$LINES $nl $DATA"

   # Resolver
   DATAPV=$RESOLVERPV
   TRIGGPV=$TESTNUMPV
   TRIGGVAL=$TESTNUMBER
   DATACOUNT=1
   DATA=$(bash ecmcGetLinesBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})   
   LINES="$LINES $nl $DATA"

   # Reference
   DATAPV=$REFERENCEPV
   TRIGGPV=$TESTNUMPV
   TRIGGVAL=$TESTNUMBER
   DATACOUNT=1
   DATA=$(bash ecmcGetLinesBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})      
   LINES="$LINES $nl $DATA"
  done
done

# Backward tests
TESTNUMBER_BASE=2
for CYCLE in $CYCLES;
do
  for TEST in $TESTS
  do   
   TESTNUMBER=$TESTNUMBER_BASE$CYCLE"0"$TEST
   
   # Target position
   DATAPV=$MOTORSETPV
   TRIGGPV=$TESTNUMPV
   TRIGGVAL=$TESTNUMBER
   DATACOUNT=1
   DATA=$(bash ecmcGetLinesBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})   
   LINES="$LINES $nl $DATA"

   # Open loop counter
   DATAPV=$MOTORACTPV
   TRIGGPV=$TESTNUMPV
   TRIGGVAL=$TESTNUMBER
   DATACOUNT=1
   DATA=$(bash ecmcGetLinesBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT}) 
   LINES="$LINES $nl $DATA"

   # Resolver
   DATAPV=$RESOLVERPV
   TRIGGPV=$TESTNUMPV
   TRIGGVAL=$TESTNUMBER
   DATACOUNT=1
   DATA=$(bash ecmcGetLinesBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})   
   LINES="$LINES $nl $DATA"

   # Reference
   DATAPV=$REFERENCEPV
   TRIGGPV=$TESTNUMPV
   TRIGGVAL=$TESTNUMBER
   DATACOUNT=1
   DATA=$(bash ecmcGetLinesBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})   
   LINES="$LINES $nl $DATA"
  done
done

echo "$LINES"
