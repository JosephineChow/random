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
    TCP_PORT = int(sys.argv[2])
else: # nothing is supplied
    print "Defaulting to localhost"
    TCP_IP = '127.0.0.1'
    TCP_PORT = 5007

	
BUFFER_SIZE = 500000

def syn_test(f,sock):
    global count
    request = f.read(500) # get 500 bytes from /dev/random to avoid compression
    sock.send(request) # send request 
    # data = sock.recv(BUFFER_SIZE) # recv 5 kilo bytes response from server
    # print(data[0])
    data = bytearray()
    n = BUFFER_SIZE
    try:
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
    except Exception as e: 
        print("something went wrong!")
        print(e)

def connect_ec2():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(TCP_IP,TCP_PORT)
    s.connect((TCP_IP,TCP_PORT))
    return s 

sock = connect_ec2() 
print("connected")
f = open("/dev/random")
for i in range(0,250): # 10 requests 
    syn_test(f,sock)
f.close()
sock.close()



