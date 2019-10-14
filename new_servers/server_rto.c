#include <stdio.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <pthread.h>
#include <netinet/tcp.h>


static const int MAXPENDING = 100; // Maximum outstanding connection requests
void *HandleTCPClient(void* sock);
void bytes_exchange(int sock);
void bytes_read_from_file(char *buff);


/*
	Read 5 kilo bytes from /dev/random
*/
void bytes_read_from_file(char *buff) {
	FILE *fileptr;
	fileptr = fopen("/dev/random","rb");
	fread(buff, 5000, 1, fileptr); 
}//end bytes_read_from_file 


/*
	Every time we get 500 bytes from client, we should send 5 kilobytes back
*/
void bytes_exchange(int sock) {
	int totalRecv = 0;
	int num_bytes_rcv = 500;
	char buff[500];
	char random[5000];
	bytes_read_from_file(random);
	while (totalRecv < num_bytes_rcv) {
		totalRecv += recv(sock, buff+totalRecv, num_bytes_rcv-totalRecv, 0);
	}//end while
	// ssize_t send(int sockfd, const void *buf, size_t len, int flags);
	send(sock,random,5000,0);
}//end bytes_exchange

void *HandleTCPClient(void* sock) {
	printf("Hello\n");
	int socket = (int) sock;
	struct tcp_info info;
	socklen_t info_size = sizeof(info);
	if (getsockopt(socket, SOL_TCP, TCP_INFO, (void *) &info, &info_size) == 0) {
		// in microseconds.. ? u? 
		struct tm *tm_struct = localtime(time(NULL));

		//printf("RTO: %f\n", info.tcpi_rto/1000000.);
        //printf("RTT: %f\n", info.tcpi_rtt/1000000.);

        //timestamp(M-D-Y,h:m:s) tcpi_rto tcpi_rtt tcpi_rttvar __tcpi_ato 
        printf("%d-%d-%d,%d:%d:%d \t%f\t%f\t%f\t%f\n",
        	tm_struct->tm_mon, tm_struct->tm_mday, tm_struct->tm_year,
        	tm_struct->tm_hour, tm_struct->tm_min, tm_struct->tm_sec,
        	info.tcpi_rto/1000000., info.tcpi_rtt, info.tcpi_rttvar, info.tcpi_ato);
	}//end if
	bytes_exchange(socket);
	close(socket);
	pthread_exit(0);
	return 0;
}//end HandleTCPClient

int main(int argc, char** argv) {
	int port;
	// take in a port from argv 
	if (argc == 2) {
		port = atoi(argv[1]);
	} //end if
	else {
		//exit(1);
		port = 5007;
	} //end else

	// Create socket for incoming connections
	int servSock; // Socket descriptor for server
	if ((servSock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0) {
		printf("Cannot create socket");
		exit(-1);
	} //end if

	// Fill in desired endpoint address
	// Construct local address structure
	struct sockaddr_in servAddr; // Local address
	memset(&servAddr, 0, sizeof(servAddr)); // Zero out structure
	servAddr.sin_family = AF_INET; // IPv4 address family
	servAddr.sin_addr.s_addr = htonl(INADDR_ANY); // Any incoming interface
	servAddr.sin_port = htons(port); // Local port
	
	// Bind to the local address
	if (bind(servSock, (struct sockaddr*) &servAddr, sizeof(servAddr)) < 0) {
		printf("Cannot bind to local address");
		exit(0);

	}//end if


	// set the socket to LISTEN
	// Mark the socket so it will listen for incoming connections
	if (listen(servSock, MAXPENDING) < 0) {
		printf("Socket refuses to listen");
		exit(0);
	}//end if

	pthread_t thread_id;

	for (;;) { // Run forever
		// accept an incoming connection
		struct sockaddr_in clntAddr; // Client address
		// Set length of client address structure (in-out parameter)
		socklen_t clntAddrLen = sizeof(clntAddr);
		// Wait for a client to connect
		// The second argument points to a sockaddr_in structure, 
		// and the third argument is a pointer to the length of that 
		// structure. Upon success, the sockaddr_in contains the 
		// Internet address and port of the client to which the 
		// returned socket is connected
		int clntSock = accept(servSock, (struct sockaddr *) &clntAddr, &clntAddrLen);
		if (clntSock < 0)
			return -1;

		// clntSock is connected to a client!
		char clntName[INET_ADDRSTRLEN]; // String to contain client address

		//inet_ntop: takes the binary representation of the client’s address and converts it to a dotted-quad string.
		if (inet_ntop(AF_INET, &clntAddr.sin_addr.s_addr, clntName, sizeof(clntName)) != NULL) {
			//printf("Handling client %s/%d\n", clntName, ntohs(clntAddr.sin_port));
        }//end if
		else
			puts("Unable to get client address");
		

		if (pthread_create(&thread_id, NULL, HandleTCPClient, (void *) clntSock) < 0) {
			printf("Cannot create thread");
			exit(0);
		}//end if
		if (pthread_detach(thread_id)!=0) {
			printf("Cannot detach thread");
			exit(0);
		}//end if
	}
	// NOT reached
	return -1;
} //end main

