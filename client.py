import threading
import socket
import sys
import re

fileName = "PROJ2-HNS.txt"
resolved = open("RESOLVED.txt", "w+")

def findHosts(clientSocket,tsListenPort):
	#Send PROJI-HNS.txt one line at a time to server and receive output to print
	fileObject = open(fileName, "r")
	for line in fileObject:
		#rstrip removes ALL trailing whitespace
		line = line.rstrip()

		clientSocket.send(line) #Send line and wait for response
		print("Send: " + line)

		data = clientSocket.recv(256)
		
		#check line below this
		print("Received: " + data)
		resolved.write(data + '\n')

	fileObject.close()
	return

def main():
	#client takes in lsHostname lsListenPort
	if len(sys.argv) != 3:
		print("Invalid arguments")
		exit()

	if not sys.argv[2].isdigit():
		print("Invalid arguments")
		exit()

	lsHostname = sys.argv[1]
	lsListenPort = int(sys.argv[2])

	try:
		clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as err:
		print('LS Socket open error: {} \n'.format(err))
		exit()

	# connect to the server on local machine
	server_binding = (socket.gethostbyname(lsHostname), lsListenPort)
	clientSocket.connect(server_binding)

	findHosts(clientSocket, lsListenPort)

	# disconnect from rs	
	clientSocket.close()
	print("RESOLVED.txt is setup")
	exit()

main()
