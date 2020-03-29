import time
import socket
import sys
import re
import select

timeout = 5

def connectToTS():
	global serverToTS1Socket
	global serverToTS2Socket

	# setup socket for TS1
	try:
		serverToTS1Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as err:
		print("Server to TS1 socket open error: {}".format(err))
		exit()

	hostname = sys.argv[2]
	port = int(sys.argv[3])

	# connect to TS1
	binding = (socket.gethostbyname(hostname), port)
	serverToTS1Socket.connect(binding)

	# setup socket for TS1
	try:
		serverToTS2Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as err:
		print("Server to TS2 socket open error: {}".format(err))
		exit()

	hostname = sys.argv[4]
	port = int(sys.argv[5])

	# connect to TS2
	binding = (socket.gethostbyname(hostname), port)
	serverToTS2Socket.connect(binding)

def handleQuery(message):
	# check if pending recv from TS1 or TS2 to clear
	# in case both TS1 and TS2 responded to a previous message
	# is this necessary?

	# send message to both TS
	serverToTS1Socket.send(message)
	serverToTS2Socket.send(message)

	# wait for first response or 5 seconds
	readable = select.select([serverToTS1Socket, serverToTS2Socket], [], [], timeout)
	if readable[0]:
		return readable[0][0].recv(256)
	else:
		return (message + " - Error:HOST NOT FOUND")

def handleClient():
	# listen and accept first client
	serverToClientSocket.listen(1)
	print("Awaiting client")
	clientConnection, clientAddress = serverToClientSocket.accept()
	print("Accepted client")

	# waits up to 5 seconds for clientConnection to be readable
	readable = select.select([clientConnection], [], [], timeout)
	while readable[0]:
		# receive from client
		message = clientConnection.recv(256)

		# close connection if no message
		if len(message) == 0:
			break;

		# handle message and reply
		response = handleQuery(message)
		clientConnection.send(response)

		# waits up to 5 seconds for next message
		readable = select.select([clientConnection], [], [], timeout)

	# loop ends when timed out
	print("Closed client connection")
	return

def main():
	global serverToClientSocket

	if len(sys.argv) != 6:
		print("Invalid arguments")
		exit()

	if (not sys.argv[1].isdigit()) or (not sys.argv[3].isdigit()) or (not sys.argv[5].isdigit()):
		print("Invalid arguments")
		exit()

	# port for server-client connection
	serverToClientlistenPort = int(sys.argv[1])

	# create server-client socket
	try:
		serverToClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as err:
		print("Server to Client socket open error: {}".format(err))
		exit()

	# bind server-client socket to listen
	binding = ('', serverToClientlistenPort)
	serverToClientSocket.bind(binding)

	# create and connect to TS1 and TS2
	connectToTS()

	while True:
		# wait for and handle clients one at a time
		handleClient()

	# never reached
	serverToClientSocket.close()
	exit()

main()
