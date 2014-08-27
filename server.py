import os,sys
sys.path.append("."+os.path.sep+"server")
from socket import *
from task import *
from ThreadManager import *
from ServerReceiveTask import *

if __name__ == '__main__':

	host = "localhost"
	port = 8973
	socket = socket(AF_INET, SOCK_STREAM)
	socket.bind((host, port))
	socket.listen(5000)

	while(True):
		tempSocket,address = socket.accept()
		serverReceiveTask = ServerReceiveTask(tempSocket,address)
		serverReceiveTask.run()
