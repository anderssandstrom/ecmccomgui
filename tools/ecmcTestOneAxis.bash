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
python ecmcTestHome.py ${motorPV} ${testPV} 1 10

echo "2. Starting low limit jitter test.."
python ecmcTestLimitBwd.py ${motorPV} ${testPV} 2 $velo 2000

echo "3.1 Starting repeatability test pos 15 (from below).."
python ecmcTestRepeatability.py ${motorPV} ${testPV} 13 15 $velo 3100

echo "3.2 Starting repeatability test pos 15 (from above).."
python ecmcTestRepeatability.py ${motorPV} ${testPV} 17 15 $velo 3200

echo "3.3 Starting repeatability test pos 35 (from below).."
python ecmcTestRepeatability.py ${motorPV} ${testPV} 33 35 $velo 3300

echo "3.4 Starting repeatability test pos 35 (from above).."
python ecmcTestRepeatability.py ${motorPV} ${testPV} 37 35 $velo 3400

echo "1. Starting resolver standstill jitter test.."
python ecmcTestResolver.py ${motorPV} ${testPV} 0.125 8 $velo 1000

echo "3.5 Starting repeatability test pos 55 (from below).."
python ecmcTestRepeatability.py ${motorPV} ${testPV} 53 55 $velo 3500

echo "3.6 Starting repeatability test pos 55 (from above).."
python ecmcTestRepeatability.py ${motorPV} ${testPV} 57 55 $velo 3600

echo "4. Starting high limit jitter test.."
python ecmcTestLimitFwd.py ${motorPV} ${testPV} 2 $velo 4000

echo "5. Scan backward to low limit.."
python ecmcTestScanBwd.py ${motorPV} ${testPV} $velo 200 5000

echo "6. Scan forward to high limit.."
python ecmcTestScanFwd.py ${motorPV} ${testPV} $velo 200 6000

echo "7. Step backward to low limit.."
python ecmcTestStepScan.py ${motorPV} ${testPV} 60 5 5 $velo 7000

echo "x.x Move to pos 3 to get correct dir to approach pos 5 in test 8.."
python ecmcTestMovePos.py ${motorPV} 3 $velo

echo "8. Step forward to high limit.."
python ecmcTestStepScan.py ${motorPV} ${testPV} 5 60 5 $velo 8000

echo "Tests finalized, please stop data acquisition.."
