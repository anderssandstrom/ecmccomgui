#!/bin/bash
# 
# Calc standard dev of elements in a row
#
# Arg 1 Optional file name, otherwise stdin
#
# Return Average value
#
# Example: Std all data in a row
# bash ecmcAvgData.bash
#
# Author: Anders Sandström, anders.sandstrom@esss.se
#

FILE="-"
if [ "$#" -eq 1 ]; then
    FILE=$1
fi

if [ "$#" -gt 1 ]; then
  echo "ecmcStdDataRow: Wrong arg count..."
  exit 1  
fi

STD=$(cat ${FILE} | awk 'NF>1{ s=0;s2=0;c=NF ;
           for (i=1; i<=NF;i++) { s+=$i ; s2+=$i*$i;}
           # compute sd from c,s and s2
           printf "%f\n",sqrt((s2/c)-(s/c)^2) ;}')
echo "${STD}"

