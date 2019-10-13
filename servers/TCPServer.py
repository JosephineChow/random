#!/usr/bin/env python2.7
import socket
import threading
import os
import numpy as np
import re
import time
from scapy.all import *

ACK = 0x10
PSH = 0x08
SYN = 0x02
FIN = 0x01
PSHACK = PSH + ACK
FINACK = ACK+FIN
SYNACK = ACK+SYN
cardName = "eth0"
a = []
counter = 0
with open("gif") as myfile:
    contents = myfile.read() 


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
            threading.Thread(target=self.listenToClient, args=(client, address)).start()

    def listenToClient(self, client, address):
        global counter
        rtts = []
        print address[0]
        prefix = "pcaps/" + address[0]

        os.system("tcpdump -i " + cardName + " -G 15 -W 1 host " + address[0] + " -w pcaps/" + address[0] + ".pcap &")
        os.system("ping -c 15 " + address[0] + " > pcaps/" + address[0] + "_server_ping.txt &")
        time.sleep(1.5)
        print "tcpdump -G 30 -W 1 host " + address[0] + " -w pcaps/" + address[0] + ".pcap &"
        for i in range(100):
            counter += 1
            client.send(str(counter) + " " + contents)
            time.sleep(.15)    
        #time.sleep(1) # Can we use pexpect or something to do this instead of just waiting? I mean it works..

        server_ping = []
        with open(prefix+"_server_ping.txt", "r") as f:
            for line in f:
                ping_time = re.search('time=(\d+\.*\d*) ms', line)
                if ping_time:
                    server_ping.append(float(ping_time.groups()[0]))
                if len(server_ping) == 200:
                    break

        # We've now written both out. How do we determine RTT?
        toServerPackets = {}  # Contains Acknum:pkt of packets to the server
        toClientPackets = {}  # Contains Seqnum:pkt of packets to the client
        for pkt in PcapReader("pcaps/" + address[0] + ".pcap"):
            if TCP in pkt:
                flag = pkt[TCP].flags

                if flag == ACK or flag == PSHACK:
                    # ACK implies data - but is it ever going to be PSH, ACK?
                    src = pkt[IP].src
                    dst = pkt[IP].dst
                    if dst == address[0]:
                        # Put the packets in the client packets
                        # Want the sequence number
                        if pkt[TCP].seq not in toClientPackets:
                            toClientPackets[pkt[TCP].seq] = pkt
                    elif src == address[0]:
                        # Want the ack number
                        if pkt[TCP].ack not in toServerPackets:
                            toServerPackets[pkt[TCP].ack] = pkt

        #  Go through the packets to the client and determine if there is a corresponding ACK
        for seqnum in toClientPackets:
            pkt = toClientPackets[seqnum]

            # The following two lines are a guess I found online
            tcp_header_len = pkt.getlayer(TCP).dataofs * 32 / 8 
            tcp_seg_len= len(pkt) - tcp_header_len - 34  # Not good george you need to fix this
            # print "Seqnum"
            # print seqnum
            # print "TCP length"
            # print tcp_seg_len
            if seqnum+tcp_seg_len in toServerPackets:
                rtts.append(1000*(toServerPackets[seqnum+tcp_seg_len].time-pkt.time))

        # print toClientPackets.keys()
        print sorted(rtts)
        print rtts
        print "Results for", prefix
        print "\nHandshakes"
        print "\tLength: " + str(len(rtts))
        print "\thandshakes_min: %.10f" % min(rtts)
        print "\thandshakes_max: %.10f" % max(rtts)
        print "\thandshakes_average: %.10f" % np.mean(rtts)
        print "\thandshakes_median: %.10f" % np.median(rtts)
        print "\nServer ping"
        print "\tserver_ping_min: %.10f" % min(server_ping)
        print "\tserver_ping`_max: %.10f" % max(server_ping)
        print "\tserver_ping_average: %.10f" % np.mean(server_ping)
        print "\tserver_ping_median: %.10f" % np.median(server_ping)
        print "\n"
        print "handshakes_min - server_ping_min %.10f" % (min(rtts) - min(server_ping))
        print "handshakes_average - server_ping_average %.10f" % (np.mean(rtts) - np.mean(server_ping))
        print "handshakes_median - server_ping_median %.10f" % (np.median(rtts) - np.median(server_ping))
        print "handshakes_max - server_ping_max %.10f\n" % (max(rtts) - max(server_ping))
        
        if min(rtts) - min(server_ping) < 10:
            client.send("You're probably not using a VPN.")
        else:
            client.send("You're probably using a VPN, about %.3f ms away\n" % (min(rtts) - min(server_ping)))

        client.shutdown(socket.SHUT_RDWR)
        client.close()


if __name__ == "__main__":
    port_num = 5006
    ThreadedServer('', port_num).listen()
