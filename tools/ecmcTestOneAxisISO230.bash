#!/bin/bash

#################################### DEFINITIONS 
motorPV="IOC_TEST:Axis1"
testPV="IOC_TEST:TestNumber"
VELO=0.75

# TEST Positions 15,25,35,45,55
FIRST_TEST_POS=15
LAST_TEST_POS=55
POS_STEP=10
RESOLVER_TEST_POS=35

# Approach first test position from 10
START_POS=10

# Approch last test from when going backward
END_POS=60


#################################### FUNCTIONS
# No functions yet



#################################### MAIN


## PREPS
# Calc how many positions to tests
POS_COUNTER=$((($LAST_TEST_POS-$FIRST_TEST_POS)/$POS_STEP+1))

echo "POS_COUNT: $POS_COUNTER"
echo "Starting ecmc automatic FAT/SAT script!"

echo "0.0 Initilize tests..."
# Toggle so zero will get new timestamp
python ecmcTestInit.py ${testPV} -10
python ecmcTestInit.py ${testPV}  0

read -p "Ready to start the tests (Y/N) (if yes then please start data acquisition)? " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi

echo "0.1 Homing with sequence 1 (to low limit)..."
#python ecmcTestHome.py ${motorPV} ${testPV} 1 10


# ISO 230-2 test series
# Go to xx positions over stroke 5 times (allow max 99 positions otherwise testnumber will overflow)
# The testnumber is encoded like this <dir><cycle><position_2_dig>
#  <dir> = 1: Forward
#  <dir> = 2: Backward
#  <cycle> = 1..5 for the cycles
#  <position_2_dig> = 01..0x for the position

# A few examples:
# position 1101 is the first target position approached from below in test cycle 1
# position 2403 is the third target position approached from above in test cycle 4
#
# Cycle 1
# p forward  1101 1102 1103 1104 1105
# p backward 2101 2102 2103 2104 2105
# Cycle 2
# p forward  1201 1202 1203 1204 1205
# p backward 2201 2202 2203 2204 2205

# So position 8205 have same target as 7201 bot approched from different directions
echo "1..2. Starting test sequence according to ISO 230-2 (5 cycles ).."
for CYCLE in {1..5};
do
   echo "*********************NEW CYCLE***********************************"
   echo "CYCLE = $CYCLE"

   # Go to start position
   echo "Go to start position ($START_POS)..."
   python ecmcTestMovePos.py ${motorPV} $START_POS $VELO

   TESTNUMBER=1"$CYCLE"00
   echo "Start scan forward... ($FIRST_TEST_POS .. $LAST_TEST_POS step $POS_STEP).."
   python ecmcTestStepScanISO230.py ${motorPV} ${testPV} $FIRST_TEST_POS $LAST_TEST_POS $POS_STEP $VELO $TESTNUMBER 1

   # Go to end position
   echo "Go to end position... ($END_POS)..."
   python ecmcTestMovePos.py ${motorPV} $END_POS $VELO

   # Calc testnumber to correlate to forward positons in a better way
   TESTNUMBER=2"$CYCLE"00
   TESTNUMBER=$(($TESTNUMBER + $POS_COUNTER+1))
   echo "Start scan backward... ($LAST_TEST_POS..$FIRST_TEST_POS step $POS_STEP).."
   python ecmcTestStepScanISO230.py ${motorPV} ${testPV} $LAST_TEST_POS $FIRST_TEST_POS $POS_STEP $VELO $TESTNUMBER 0

done

echo "3. Starting low limit jitter test.."
python ecmcTestLimitBwd.py ${motorPV} ${testPV} 2 $VELO 3000

echo "Go to resolver test position... ($RESOLVER_TEST_POS)..."
python ecmcTestMovePos.py ${motorPV} $RESOLVER_TEST_POS $VELO

echo "4. Starting resolver standstill jitter test.."
python ecmcTestResolver.py ${motorPV} ${testPV} 0.125 8 $VELO 4000

echo "5. Starting high limit jitter test.."
python ecmcTestLimitFwd.py ${motorPV} ${testPV} 2 $VELO 5000

echo "6. Jog backward to low limit.."
python ecmcTestScanBwd.py ${motorPV} ${testPV} $VELO 200 6000

echo "7. Jog forward to high limit.."
python ecmcTestScanFwd.py ${motorPV} ${testPV} $VELO 200 7000

echo "Tests finalized, please stop data acquisition.."
