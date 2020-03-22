import time
import socket
import sys
import re
import select

def main():
	if len(sys.argv) != 3:
		print("Invalid arguments")
		exit()

	# get port
	listenPort = int(sys.argv[1])

	# create socket
	try:
		ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as err:
		print("TS Socket open error: {}".format(err))
		exit()

	# bind to listen
	binding = ('', listenPort)
	ss.bind(binding)

	# listen
	ss.listen(1)
	print("Listening")

	connection, clientAddress = ss.accept()
	print("Accepted")

#	print("Awaiting Data")
#	readable, writable, exceptional = select.select([connection], [], [], float(sys.argv[2]))
#	if connection in readable:
#		data = connection.recv(256)
#		print("Recieved: " + data)
#	else:
#		data = connection.recv(256)
#		print("Timed out and received: " + data)

	connection.send("ok ok ok")
	ss.close()
	exit()

main()
