#!/bin/bash

# This script takes 2 arguments, 1) naming convention 2) VPN IP 


sudo pkill tcpdump
nohup python2 server.py &
nohup sudo tcpdump host $2 and port 5005 and tcp -w $1_server.pcap >/dev/null 2>&1 &
