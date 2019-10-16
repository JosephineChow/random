#!/bin/bash


#ssh -i "aws_dave.pem" -vvv ubuntu@$1.compute.amazonaws.com "touch hi.txt"
START="
yum install git && 
yum install gcc && 
git clone https://github.com/josephinechow/random &&
cd /random/new_servers &&
gcc -pthread rto_server.c -o rto &&
./rto &
"
ssh -i "aws_dave.pem" -o StrictHostKeyChecking=no ec2-user@$1.compute.amazonaws.com $START





