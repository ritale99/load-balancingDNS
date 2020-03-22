import time
import socket
import sys
import re

addresses = {}
fileName = "PROJ2-DNSTS1.txt"

def buildData():
	global addresses

	fileObject = open(fileName, "r")
	#makes a list of each line in file
	data = fileObject.readlines()

	for line in data:
		#splits the line into hostname, ip, flag
		lineData = line.split(" ")

		hostName = lineData[0].lower()
		ip = lineData[1]
		flag = re.search(r"\w+", lineData[2]).group()

		#store in dictionary
		addresses[hostName] = ip

def handleQuery(inputString, connection):
	#check if in dictionary of dns
	#if in dictionary, send Hostname ip and A
	#else, don't send anything

	#format to response message if ip found
	if inputString.lower() in addresses:
		response = inputString.lower() + " " + addresses[inputString] + " A"
		print("Response: " + response)
		connection.send(response)
	return

def handleLS():
	# Wait for query, then handle
	print("Awaiting LS")
	connection, LSAddress = TS2LSSocket.accept()
	print("Accepted LS")

	while True:
		data = connection.recv(256) #note, host names are assumed to be <200 chars

		print("Received: " + data)

		# Close connection if no message
		if len(data) == 0:
			print("No message, closing connection")
			break

		# Handle message and reply
		handleQuery(data, connection)

	return

def main():
	global TS2LSSocket

	if len(sys.argv) != 2:
		print("Invalid arguments")
		exit()

	if not sys.argv[1].isdigit():
		print("Invalid arguments")
		exit()

	tsListenPort = int(sys.argv[1])

	#create the socket
	try:
		TS2LSSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as err:
		print('TS socket open error: {}'.format(err))
		exit()

	#bind socket for listening
	binding = ('', tsListenPort)
	TS2LSSocket.bind(binding)

	#listen for connection
	TS2LSSocket.listen(1)
	host = socket.gethostname()
	print("TS host name: {}".format(host))
	print("TS port: {}".format(tsListenPort))

	#localhost = socket.gethostbyname(host)

	#Load data
	buildData()

	# wait for and handle ls one at a time
	while True:
		handleLS()

	# Close the server socket, never?
	TS2LSSocket.close()
	exit()

main()
