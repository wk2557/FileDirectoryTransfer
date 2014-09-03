import os, sys
sys.path.append("../common/")
from socket import *
from struct import *
from Task import *

class ClientReceiveTask(Task):
	def __init__(self, destHost, destPort):
		self.destHost = destHost
		self.destPort = destPort
		self.maxBufferSize = 8 * 1024
		self.command = '-r'
		self.socket = socket(AF_INET, SOCK_STREAM)
		print("init: destination host and port are %s:%s" % (destHost, destPort))

	def SetDestHostAndPort(self, destHost, destPort):
		self.destHost = destHost
		self.destPort = destPort
		print("SetDestHostAndPort: destination host and port are %s:%s" % (destHost, destPort))
	
        def SetSourAndDestDir(self, sourDir, destDir):
                self.sourDir = sourDir.strip(' \t')
                if self.sourDir[-1] == os.path.sep:
                        self.sourDir = self.sourDir[0:-1]
                print('source is %s' % self.sourDir)

                if not os.path.exists(self.sourDir):
                        print('source directory or file %s does not exist!\n' % self.sourDir)
                        return

                self.destDir = destDir.strip(' \t')
                if self.destDir[-1] == os.path.sep:
                        self.destDir = self.destDir[0:-1]
                print('destination is %s' % self.destDir)


	def ValidateFile(self, filePath):
		directory, fileName = os.path.split(filePath)
		if not os.path.exists(directory):
			os.makedirs(directory)

	def run(self):
		self.socket.connect((self.destHost, self.destPort))
		self.socket.send(self.command)
		head = pack('!128s128s', self.sourDir, self.destDir)
		self.socket.send(head)

		while True:
			headLength = calcsize('!128sI')
			head = self.socket.recv(headLength)
			if not head or len(head) == 0:
				break
			fileName, fileSize = unpack('!128sI', head)
			fileName = fileName.strip('\00')
			#print('filename and size is %s %d' % (fileName,fileSize))
			if fileSize == 0:
				continue

			self.ValidateFile(fileName)
			file = open(fileName, 'wb')

			while(True):
				if fileSize <= self.maxBufferSize:
					receiveSize = fileSize
				else:
					receiveSize = self.maxBufferSize

				body = self.socket.recv(receiveSize)
				#print('body is %s' % body)

				file.write(body)
				fileSize -= len(body)
				#print('%d byes of data are needed to be received' % fileSize)

				if fileSize <= 0:
					file.close()
					break
				
		self.socket.close()

