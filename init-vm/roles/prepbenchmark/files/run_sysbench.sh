#!/bin/bash

LOG=/tmp/sysbench.log
while true ; do
    RES=$(/usr/bin/sysbench --test=cpu --cpu-max-prime=20000 run)
    date >> $LOG
    echo "------------------------" >> $LOG
    echo $RES >> $LOG
done
