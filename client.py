import os, sys
sys.path.append("./client")
sys.path.append("./common")
from socket import *
from Task import *
from ThreadManager import *
from ClientSendTask import *

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print ("not enough args, please input source, des-machine and des-path")
		sys.exit()

	destHost = sys.argv[1]
	destPort = 8973
	sourDir = sys.argv[2]
	destDir = sys.argv[3]

	clientSendTask = ClientSendTask(destHost, destPort)
	clientSendTask.SetSourAndDestDir(sourDir, destDir)

	clientSendTask.run()
