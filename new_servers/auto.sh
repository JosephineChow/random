#!/bin/bash

# this script takes 1) EC2 server to connect to, 2) Naming convention

VPN=`curl -s https://ifconfig.co`


SETUP="
sudo yum -y install git &&
sudo yum -y install gcc &&
git clone https://github.com/josephinechow/random > out.txt 2>err.txt 
"

ssh -i "aws_dave.pem" -o StrictHostKeyChecking=no ec2-user@$1.compute.amazonaws.com $SETUP


# setup.sh takes naming convention then VPN's IP address 
ssh -i "aws_dave.pem" -o StrictHostKeyChecking=no ec2-user@$1.compute.amazonaws.com  "cd random/new_servers && ./first.sh $2 $VPN"


echo 'about to spin up client rto'
./client_rto.py $1.compute.amazonaws.com

echo 'finished running client rto'
ssh -i "aws_dave.pem" -o StrictHostKeyChecking=no ec2-user@$1.compute.amazonaws.com "cd random/new_servers && ./second.sh $2 $VPN"


echo 'about to spin up client tcp handshakes'
./client.py $1.compute.amazonaws.com


ssh -i "aws_dave.pem" -o StrictHostKeyChecking=no ec2-user@$1.compute.amazonaws.com 'sudo pkill tcpdump'









