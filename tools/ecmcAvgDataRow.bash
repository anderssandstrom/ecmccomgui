#!/bin/bash
# 
# Calc average of elements in a row
#
# Arg 1 Optional file name, otherwise stdin
#
# Return Average value
#
# Example: Avg values in a row
# bash ecmcAvgData.bash
#
# Author: Anders Sandström, anders.sandstrom@esss.se
#

FILE="-"
if [ "$#" -eq 1 ]; then
    FILE=$1
fi

if [ "$#" -gt 1 ]; then
  echo "ecmcAvgDataRow: Wrong arg count..."
  exit 1  
fi

AVG=$(cat ${FILE} | awk '{sum = 0; for (i = 1; i <= NF; i++) sum += $i; sum /= NF; print sum}')
echo "${AVG}"
