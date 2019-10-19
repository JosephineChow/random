#!/bin/bash


#ssh -i "aws_dave.pem" -vvv ubuntu@$1.compute.amazonaws.com "touch hi.txt"

VPN=`curl -s https://ifconfig.co`

#rm -rf random/ &&


#
#sudo yum -y install git && 
#sudo yum -y install gcc && 
#git clone https://github.com/josephinechow/random > out.txt 2>err.txt &&

START="
cd random/new_servers &&
rm -f ip.txt && 
ping $VPN -c 100 > $2_server_ping.txt && 
gcc -pthread rto_server.c -o rto > out.txt 2>err.txt &&
touch pre_rto.txt &&
nohup ./rto > $2_rto.txt &:; 
touch post_rto.txt &&
sudo nohup tcpdump host $VPN and port 5007 and tcp -w $2_rto_server.pcap &:;
touch post_tcpdump.txt
"
ssh -i "aws_dave.pem" -o StrictHostKeyChecking=no ec2-user@$1.compute.amazonaws.com $START


#add me in 
#sudo tcpdump host $1.compute.amazonaws.com and port 5007 and tcp &
echo 'about to spin up client rto'
./client_rto.py $1.compute.amazonaws.com


HANDSHAKE="
cd random/new_servers &&
sudo pkill tcpdump
nohup python2 server.py &:;
sudo nohup tcpdump host $VPN and port 5005 and tcp -w $2_server.pcap &:;
sudo pkill tcpdump
"
ssh -i "aws_dave.pem" -o StrictHostKeyChecking=no ec2-user@$1.compute.amazonaws.com $HANDSHAKE


./client.py $1.compute.amazonaws.com









