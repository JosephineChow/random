#!/bin/bash

# this script takes 1) EC2 server to connect to, 2) Naming convention

VPN=`curl -s https://ifconfig.co`


# setup.sh takes naming convention then VPN's IP address 
ssh -i "aws_dave.pem" -o StrictHostKeyChecking=no ec2-user@$1.compute.amazonaws.com ./first.sh $2 $VPN 


echo 'about to spin up client rto'
./client_rto.py $1.compute.amazonaws.com


ssh -i "aws_dave.pem" -o StrictHostKeyChecking=no ec2-user@$1.compute.amazonaws.com ./second.sh $2 $VPN


echo 'about to spin up client tcp handshakes'
./client.py $1.compute.amazonaws.com


ssh -i "aws_dave.pem" -o StrictHostKeyChecking=no ec2-user@$1.compute.amazonaws.com 'sudo pkill tcpdump'









