#!/bin/bash

# This script takes 2 arguments, 1) naming convention 2) VPN IP 


cd random/new_servers
sudo pkill tcpdump
nohup python2 server.py &
sudo nohup tcpdump host $2 and port 5005 and tcp -w $1_server.pcap &