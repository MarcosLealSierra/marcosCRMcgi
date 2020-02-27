#!/bin/bash

declare -i seconds=1440
declare -i tiempo

for archivo in /tmp/pysession/*; do
   tsfile=`stat -c %X $archivo`
   actual=`date +%s`
   tiempo=actual-tsfile
   
   if [ $tiempo -gt $seconds ]; then
       rm -rf $archivo
   fi
done
