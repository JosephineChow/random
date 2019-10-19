#!/bin/bash

# This script takes 2 arguments, 1) naming convention 2) VPN IP 

echo $1 >> out.txt
echo $2 >> out.txt

rm -f ip.txt 
touch before_server_ping
ping $2 -c 100 > $1_server_ping.txt 
touch post_server_ping
gcc -pthread rto_server.c -o rto >> out.txt 2>>err.txt 

nohup ./rto > $1_rto.txt &
sudo nohup tcpdump host $2 and port 5007 and tcp -w $1_rto_server.pcap &
