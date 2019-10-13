#!/usr/bin/env python2.7
import socket
import multiprocessing
import sys
import time

if len(sys.argv) == 2:
    print "Using IP: " + sys.argv[1]
    TCP_IP = sys.argv[1]
else:
	print "Defaulting to 52.26.176.186"
	TCP_IP = '52.26.176.186' 
print TCP_IP
	
TCP_PORT = 5005
#TCP_PORT = 80
BUFFER_SIZE = 1024
#MESSAGE = "GOODBYE WOLRD"

def syn_test(num):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP,TCP_PORT))
    #s.send(MESSAGE + str(num))
    #data = s.recv(BUFFER_SIZE)
    time.sleep(1.5) 
    s.close()

threadpool = multiprocessing.Pool(20)
threadpool.map_async(syn_test, xrange(300))
threadpool.close()
threadpool.join()
