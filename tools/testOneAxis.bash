#!/bin/bash

motorPV=IOC_TEST:Axis1

echo "Starting ecmc automatic slit SAT script!"

read -p "Ready to start the tests (Y/N)? " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi

# Start with homing

