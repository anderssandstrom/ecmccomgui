#!/bin/bash

motorPV=IOC_TEST:Axis1

echo "Starting ecmc automatic slit SAT script!"

read -p "Ready to start the tests (Y/N)? " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi

echo "0. Homing with sequence 1 (to low limit)..."
python ecmcHomeAxis.py ${motorPV} 1

read -p "Please start data acquistion now!" -n 1 -r

echo "1. Starting resolver standstill jitter test.."
python ecmcTestResolver.py IOC_TEST:Axis1 IOC_TEST:TestNumber 0.125 8 0.5

echo "2. Starting low limit jitter test.."
python ecmcTestLimitBwd.py IOC_TEST:Axis1 IOC_TEST:TestNumber 1 0.5

echo "3.1 Starting repeatability test pos 15 (from below).."
python ecmcTestRepeatability.py IOC_TEST:Axis1 IOC_TEST:TestNumber 14.5 15 0.5 3100

echo "3.2 Starting repeatability test pos 15 (from above).."
python ecmcTestRepeatability.py IOC_TEST:Axis1 IOC_TEST:TestNumber 15.5 15 0.5 3500

echo "3.3 Starting repeatability test pos 35 (from below).."
python ecmcTestRepeatability.py IOC_TEST:Axis1 IOC_TEST:TestNumber 34.5 35 0.5 3200

echo "3.4 Starting repeatability test pos 35 (from above).."
python ecmcTestRepeatability.py IOC_TEST:Axis1 IOC_TEST:TestNumber 35.5 35 0.5 3600

echo "3.5 Starting repeatability test pos 55 (from below).."
python ecmcTestRepeatability.py IOC_TEST:Axis1 IOC_TEST:TestNumber 54.5 55 0.5 3300

echo "3.6 Starting repeatability test pos 55 (from above).."
python ecmcTestRepeatability.py IOC_TEST:Axis1 IOC_TEST:TestNumber 55.5 55 0.5 3700

echo "4. Starting high limit jitter test.."
python ecmcTestLimitFwd.py IOC_TEST:Axis1 IOC_TEST:TestNumber 1 0.5

echo "5. Scan backward to low limit.."
python ecmcTestJogBwd.py IOC:Axis1 IOC:TestNumber 0.5 5000

echo "6. Scan forward to hig limit.."
python ecmcTestJogFwd.py IOC:Axis1 IOC:TestNumber 0.5 6000
