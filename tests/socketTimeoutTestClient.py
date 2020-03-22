import time
import socket
import sys
import re
import select

def main():
	if len(sys.argv) != 4:
		print("Invalid arguments")
		exit()

	listenPort = int(sys.argv[1])

	# create socket
	try:
		cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as err:
		print("Client Socket open error: {}".format(err))
		exit()

	# attempt to connect to server
	binding = (socket.gethostbyname(sys.argv[2]), listenPort)
	cs.connect(binding)

	# wait
	print("Setup and sleeping")
	time.sleep(float(sys.argv[3]))

	# send data
	print("Sending")
	cs.send("test message")

	# close end exit
	cs.close()
	exit()

main()
