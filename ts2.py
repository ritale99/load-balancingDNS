import time
import socket
import sys
import re

addresses = {}
fileName = "PROJ2-DNSTS2.txt"

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
	#if not found, it will be formatted as the preset message
	if inputString.lower in addresses:
		response = inputString.lower() + " " + addresses[inputString] + " A"
		connection.send(response.encode('utf-8'))
	else:
        #FIX THIS TO SEND NOTHING
		response = inputString.lower()
	return

def main():
	if len(sys.argv) != 2:
		print("Invalid arguments")
		exit()

	if not sys.argv[1].isdigit():
		print("Invalid arguments")
		exit()

	ts1ListenPort = int(sys.argv[1])

	#create the socket
	try:
		ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as err:
		print('TS socket open error: {}'.format(err))
		exit()

	#bind socket for listening
	binding = ('', ts1ListenPort)
	ss.bind(binding)

	#listen for connection
	ss.listen(1)
	host = socket.gethostname()
	print("TS host name: {}".format(host))
	print("TS port: {}".format(ts1ListenPort))

	#localhost = socket.gethostbyname(host)

	#Load data
	buildData()

	#receive query on loop
	while True:
		#accept connection
		connection, cAddress = ss.accept()
		print ("[S]: Got a connection request from a client at {}".format(cAddress))
		data = connection.recv(256) #note, host names are assumed to be <200 chars
		handleQuery(data, connection)

	# Close the server socket, never?
	ss.close()
	exit()

main()