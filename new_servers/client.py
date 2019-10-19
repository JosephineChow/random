#!/usr/bin/env python2.7
import socket
import multiprocessing
import sys
import time

if len(sys.argv) == 3:
    print "Using IP: " + sys.argv[1]
    TCP_IP = sys.argv[1]
    TCP_PORT = int(sys.argv[2])
elif len(sys.argv) == 2:
    print "Using IP: " + sys.argv[1]
    TCP_IP = sys.argv[1]
    TCP_PORT = 5005

else:
    print "Defaulting to localhost"
    TCP_IP = '127.0.0.1'
    TCP_PORT = 5005

	
BUFFER_SIZE = 1024
#MESSAGE = "GOODBYE WOLRD"

def syn_test(num):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP,TCP_PORT))
    #s.send(MESSAGE + str(num))
    #data = s.recv(BUFFER_SIZE)
    #print("connected")
    time.sleep(1.5) 
    s.close()

threadpool = multiprocessing.Pool(20)
threadpool.map_async(syn_test, xrange(300))
threadpool.close()
threadpool.join()
