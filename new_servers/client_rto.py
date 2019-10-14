#!/usr/bin/env python2.7
import socket
import sys
import time


if len(sys.argv) == 2: # only IP is supplied
    print "Using IP: " + sys.argv[1]
    TCP_IP = sys.argv[1]
    TCP_PORT = 5007
elif len(sys.argv) == 3: # port is supplied
    print "Using IP: " + sys.argv[1]
    print "Using Port: " + sys.argv[2]
    TCP_IP = sys.argv[1]
    TCP_PORT = sys.argv[2]
else: # nothing is supplied 
	print "Defaulting to localhost"
	TCP_IP = '127.0.0.1'
    TCP_PORT = 5007

	
BUFFER_SIZE = 5000

def syn_test(f,sock):
    request = f.read(500) # get 500 bytes from /dev/random to avoid compression
    sock.send(request) # send request 
    data = sock.recv(BUFFER_SIZE) # recv 5 kilo bytes response from server

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP,TCP_PORT))
    return s 

sock = connect() 
f = open("/dev/random")
for i in range(0,10): # 10 requests 
    syn_test(f,sock)
f.close()
sock.close()



