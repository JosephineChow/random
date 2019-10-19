#!/bin/bash

# This script takes 2 arguments, 1) naming convention 2) VPN IP 

rm -f ip.txt 
ping $2 -c 10 > $1_server_ping.txt 
gcc -pthread rto_server.c -o rto
nohup ./rto > $1_rto.txt &
nohup sudo tcpdump port 5007 -w $1_rto_server.pcap >/dev/null 2>&1 &
sleep 2 

