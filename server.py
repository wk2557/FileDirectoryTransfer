import os,sys
sys.path.append("./server")
sys.path.append("./common")
from socket import *
from Task import *
from ThreadManager import *
from ServerReceiveTask import *

if __name__ == '__main__':

	host = "localhost"
	port = 8973
	socket = socket(AF_INET, SOCK_STREAM)
	socket.bind((host, port))
	socket.listen(5000)

	taskManager = TaskManager(50)
	startTime = time.clock()

	while(True):
		tempSocket,address = socket.accept()
		serverReceiveTask = ServerReceiveTask(tempSocket,address)
		taskManager.insertTask(serverReceiveTask)

	taskManager.setStop()
	endTime = time.clock()
	print(endTime - startTime)
