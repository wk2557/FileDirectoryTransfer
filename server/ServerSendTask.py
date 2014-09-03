import os
import sys
sys.path.append("../common/")
from socket import *
from struct import *
from Task import *

class ServerSendTask(Task):
	def __init__(self, socket, address):
		self.socket = socket
		self.address = address
		self.bufferSize = 8*1024

	def SetSourAndDestDir(self, sourDir, destDir):
                self.sourDir = sourDir.strip(' \t\0')
                if self.sourDir[-1] == os.path.sep:
                        self.sourDir = self.sourDir[0:-1]
                print('source is %s' % self.sourDir)

                if not os.path.exists(self.sourDir):
                        print('source directory or file %s does not exist!\n' % self.sourDir)
                        return

                self.destDir = destDir.strip(' \t\0')
                if self.destDir[-1] == os.path.sep:
                        self.destDir = self.destDir[0:-1]
                print('destination is %s' % self.destDir)


	def ParseDir(self, curDir, files):
		if len(curDir) == 0 and not os.path.isdir(self.sourDir):
			self.sourDir,file = os.path.split(self.sourDir)
			files.append(os.path.sep + file)
			return

		if os.path.isdir(self.sourDir + curDir):
			listOfFiles = os.listdir(self.sourDir + curDir)
			for theFile in listOfFiles:
				self.ParseDir(curDir + os.path.sep + theFile, files)
		else:
			files.append(curDir)

	def SendFile(self, fileName):
		sourFile = self.sourDir + fileName
		destFile = self.destDir + fileName
		if not os.path.exists(sourFile):
			print ("file: %s doesn't exist" % sourFile)
			sys.exit()
		
		#print ("begin to send file: %s" % sourFile)
		#print ("dest host and part are %s-%d" % (self.destHost,self.destPort))

		head = pack('!128sI', destFile, os.stat(sourFile).st_size)
		self.socket.send(head)
		file = open(sourFile, 'rb')
		while True:
			data = file.read(self.bufferSize)
			if not data:
				break
			self.socket.send(data)

		file.close()
		#print ("end to send file: %s" % sourFile)


	def run(self):
		length = calcsize('!128s128s')
		name = self.socket.recv(length)
		if not name or len(name) == 0:
			return

		sourDir,destDir = unpack('!128s128s', name)
		print(sourDir)
		print(destDir)
		self.SetSourAndDestDir(sourDir, destDir)
		
		fileNames = []
		self.ParseDir('', fileNames)
		#print("the files to tranfer are %s" % fileNames)

		for fileName in fileNames:
			self.SendFile(fileName)

		self.socket.close()
		print("files transferring are already completed.")
