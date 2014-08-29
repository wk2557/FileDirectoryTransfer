import os, sys
sys.path.append("./client")
sys.path.append("./common")
from socket import *
from Task import *
from ThreadManager import *
from ClientSendTask import *

if __name__ == '__main__':
	if len(sys.argv) < 4:
		print ("not enough args, please input machine name, command, source path, and des-path")
		sys.exit()

	destHost = sys.argv[1]
	destPort = 8973
	command = sys.argv[2]
	sourDir = sys.argv[3]
	destDir = sys.argv[4]

	taskManager = TaskManager(1)
	startTime = time.clock()

	if command == '-s':
		clientSendTask = ClientSendTask(destHost, destPort)
		clientSendTask.SetSourAndDestDir(sourDir, destDir)
		taskManager.insertTask(clientSendTask)
	else:
		pass
		#clientReceiveTask = ClientReceiveTask(destHost, destPort)
	
	taskManager.setStop()
	endTime = time.clock()
	print(endTime - startTime)
