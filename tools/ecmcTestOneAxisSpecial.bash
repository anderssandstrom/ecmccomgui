#!/bin/bash

# 
motorPV="IOC_TEST:Axis1"
testPV="IOC_TEST:TestNumber"
velo=0.75

echo "Starting ecmc automatic slit SAT script!"

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


echo "3.3 Starting repeatability test pos 35 (from below).."
python ecmcTestRepeatability.py ${motorPV} ${testPV} 33 35 1.5 3300

echo "x.x Move to pos 60 to get correct dir to approach pos 5 in test 8.."
python ecmcTestMovePos.py ${motorPV} 60 1.5

echo "4. Starting high limit jitter test.."
python ecmcTestLimitFwd.py ${motorPV} ${testPV} 2 0.75 4000

echo "x.x Move to pos 60 to get correct dir to approach pos 5 in test 8.."
python ecmcTestMovePos.py ${motorPV} 60 $velo

echo "4. Starting high limit jitter test.."
python ecmcTestLimitFwd.py ${motorPV} ${testPV} 2 1.3 4000

echo "x.x Move to pos 60 to get correct dir to approach pos 5 in test 8.."
python ecmcTestMovePos.py ${motorPV} 60 $velo

#
#echo "7. Step backward to low limit.."
#python ecmcTestStepScan.py ${motorPV} ${testPV} 60 5 5 $velo 7000
#
#echo "x.x Move to pos 3 to get correct dir to approach pos 5 in test 8.."
#python ecmcTestMovePos.py ${motorPV} 3 $velo
#
#echo "8. Step forward to high limit.."
#python ecmcTestStepScan.py ${motorPV} ${testPV} 5 60 5 $velo 8000

echo "Tests finalized, please stop data acquisition.."
