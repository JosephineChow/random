#!/bin/bash

# This script takes 2 arguments, 1) naming convention 2) VPN IP 

rm -f ip.txt 
ping $2 -c 100 > $1_server_ping.txt 
gcc -pthread rto_server.c -o rto >> out.txt 2>>err.txt 

nohup ./rto > $1_rto.txt &
sudo nohup tcpdump host $2 and port 5007 and tcp -w $1_rto_server.pcap &
