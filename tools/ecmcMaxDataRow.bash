#!/bin/bash
# 
# Calc max of elements in a row
#
# Arg 1 Optional file name, otherwise stdin
#
# Return Range value
#
# Example: max of value in a row
# bash ecmcMaxData.bash
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

MAX=$(cat ${FILE} | awk 'NF>1{m=$1; for (i=1; i<=NF; i++){ if ($i>m){ m=$i; }}; print m;}')
echo "${MAX}"

STD=$(cat ${FILE} | awk 'NF>1{ s=0;s2=0;c=NF ;
           for (i=1; i<=NF;i++) { s+=$i ; s2+=$i*$i;}
           # compute sd from c,s and s2
           printf "%f\n",sqrt((s2/c)-(s/c)^2) ;}')
echo "${STD}"