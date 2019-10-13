#!/usr/bin/env python2.7
import socket
import threading

a = []

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(60)
        while True:
            client, address = self.sock.accept()
            client.settimeout(15)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 1024
        #data = client.recv(size)
        """
        if data:
            # Set the response to echo back the recieved data 
            response = data
            print response
            #client.send(response)
        """
        client.close()

if __name__ == "__main__":
    port_num = 80
    ThreadedServer('',port_num).listen()
