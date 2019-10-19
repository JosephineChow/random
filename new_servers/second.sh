#!/bin/bash

# This script takes 2 arguments, 1) naming convention 2) VPN IP 

touch 1.txt
sudo pkill tcpdump
touch 2.txt
nohup sudo ./server.py &
touch 3.txt
nohup sudo tcpdump host $2 and port 5005 and tcp -w $1_server.pcap >/dev/null 2>&1 &
touch 4.txt
sleep 2
touch 5.txt
