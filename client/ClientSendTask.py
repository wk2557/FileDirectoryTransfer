import os
import sys
sys.path.append("../common/")
from socket import *
from struct import *
from Task import *

class ClientSendTask(Task):

	def __init__(self):
		pass

	def __init__(self, destHost, destPort):
		self.destHost = destHost
		self.destPort = destPort
		self.bufferSize = 8 * 1024
		self.socket = socket(AF_INET, SOCK_STREAM)		
		print("init: destination host and port are %s:%s" % (destHost, destPort))

	def SetDestHostAndPort(self, destHost, destPort):
		self.destHost = destHost
		self.destPort = destPort
		print("SetDestHostAndPort: destination host and port are %s:%s" % (destHost, destPort))
	
	def SetSourAndDestDir(self, sourDir, destDir):
		self.sourDir = sourDir
		self.destDir = destDir
		print("SetSourAndDestDir: source and destination directory are %s:%s" % (sourDir, destDir))


	def ParseDir(self, curDir, files):
		if os.path.isdir(curDir):
			listOfFiles = os.listdir(curDir)
			for theFile in listOfFiles:
				self.ParseDir(curDir + os.path.sep + theFile, files)
		else:
			files.append(curDir)

	def SendFile(self, file):
		if not os.path.exists(file):
			print ("file: %s doesn't exist" % file)
			sys.exit()
		
		print ("begin to send file: %s" % file)

		self.socket.connect((self.destHost, self.destPort))	
		head = pack('!128sI', self.destDir, os.stat(file).st_size)
		self.socket.send(head)
		fileHandler = open(file, 'rb')
		while True:
			data = fileHandler.read(self.bufferSize)
			if not data:
				break
			self.socket.send(data)

#		print ("End of send file: %s" % file)

		fileHandler.close()
		self.socket.close()


	def run(self):
		files = []
		self.ParseDir(self.sourDir, files)
		print("the files to tranfer are %s" % files)
		for file in files:
			self.SendFile(file)


