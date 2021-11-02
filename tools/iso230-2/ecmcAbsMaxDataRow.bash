#!/bin/bash
# 
# Calc abs max of elements in a row
#
# Arg 1 Optional file name, otherwise stdin
#
# Return Abs Max value
#
# Example: Abs max of value in a row
# bash ecmcAbsMaxData.bash
#
# Author: Anders Sandström, anders.sandstrom@esss.se
#

FILE="-"
if [ "$#" -eq 1 ]; then
    FILE=$1
fi

if [ "$#" -gt 1 ]; then
  echo "ecmcMaxDataRow: Wrong arg count..."
  exit 1  
fi

MAX=$(cat ${FILE} | awk 'NF>1{m=$1; for (i=1; i<=NF; i++){ val=sqrt($i*$i);if (val>m){ m=val; }}; print m;}')
echo "${MAX}"
