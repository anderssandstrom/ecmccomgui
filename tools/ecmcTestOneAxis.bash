#!/bin/bash

# 
motorPV="IOC_TEST:Axis1"
testPV="IOC_TEST:TestNumber"

echo "Starting ecmc automatic slit SAT script!"

read -p "Ready to start the tests (Y/N) (if yes then please start data acquisition)? " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi

echo "0.0 Initilize tests..."
python ecmcTestInit.py ${testPV}

echo "0.1 Homing with sequence 1 (to low limit)..."
python ecmcTestHome.py ${motorPV} ${testPV} 1 10

echo "1. Starting resolver standstill jitter test.."
python ecmcTestResolver.py ${motorPV} ${testPV} 0.125 8 0.75 1000

echo "2. Starting low limit jitter test.."
python ecmcTestLimitBwd.py ${motorPV} ${testPV} 2 0.75 2000

echo "3.1 Starting repeatability test pos 15 (from below).."
python ecmcTestRepeatability.py ${motorPV} ${testPV} 13 15 0.75 3100

echo "3.2 Starting repeatability test pos 15 (from above).."
python ecmcTestRepeatability.py ${motorPV} ${testPV} 17 15 0.75 3200

echo "3.3 Starting repeatability test pos 35 (from below).."
python ecmcTestRepeatability.py ${motorPV} ${testPV} 33 35 0.75 3300

echo "3.4 Starting repeatability test pos 35 (from above).."
python ecmcTestRepeatability.py ${motorPV} ${testPV} 37 35 0.75 3400

echo "3.5 Starting repeatability test pos 55 (from below).."
python ecmcTestRepeatability.py ${motorPV} ${testPV} 53 55 0.75 3500

echo "3.6 Starting repeatability test pos 55 (from above).."
python ecmcTestRepeatability.py ${motorPV} ${testPV} 57 55 0.75 3600

echo "4. Starting high limit jitter test.."
python ecmcTestLimitFwd.py ${motorPV} ${testPV} 2 0.75 4000

echo "5. Scan backward to low limit.."
python ecmcTestScanBwd.py ${motorPV} ${testPV} 0.75 200 5000

echo "6. Scan forward to hig limit.."
python ecmcTestScanFwd.py ${motorPV} ${testPV} 0.75 200 6000

echo "Tests finalized, please stop data acquisition.."
