#!/bin/bash


#ssh -i "aws_dave.pem" -vvv ubuntu@$1.compute.amazonaws.com "touch hi.txt"

VPN=`curl -s https://ifconfig.co`

START="
sudo yum install git && 
sudo yum install gcc && 
rm -rf random/ &&
git clone https://github.com/josephinechow/random &&
cd random/new_servers &&
touch hello.txt &&
rm -f ip.txt && 
touch hi.txt
ping $VPN -c 100 > $2_server_ping.txt && 
gcc -pthread rto_server.c -o rto &&
nohup ./rto > $2_rto.txt &;
sudo nohup tcpdump host $VPN and port 5007 and tcp -w $2_rto_server.pcap &
"
ssh -i "aws_dave.pem" -o StrictHostKeyChecking=no ec2-user@$1.compute.amazonaws.com $START

#add me in 
#sudo tcpdump host $1.compute.amazonaws.com and port 5007 and tcp &

./client_rto.py $1.compute.amazonaws.com


HANDSHAKE="
cd /random/new_servers &&
sudo pkill tcpdump
nohup python2 server.py &;
sudo nohup tcpdump host $VPN and port 5005 and tcp -w $2_server.pcap &;
sudo pkill tcpdump
"
ssh -i "aws_dave.pem" -o StrictHostKeyChecking=no ec2-user@$1.compute.amazonaws.com $HANDSHAKE


./client.py $1.compute.amazonaws.com









