#!/bin/bash 

echo running iperf-client

#TODO: add your code
c=1
while [ $c ]
do
    iperf -c 10.0.0.1 -b 10M -t 0.2 -p 5001 -u &
    sleep 1
    (( c++ ))
done
#-t: time in seconds to transmit for: less than period but 1 s min?
#-i: output interval, leave as 1 s?
#-l: length in bytes, 2x bandwidth so 20Mb? = 
