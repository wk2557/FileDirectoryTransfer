import os
import sys
from socket import *
from struct import *
from Task import *

class ServerReceiveTask(Task):
	def __init__(self, socket, address):
		self.socket = socket
		self.address = address
		self.maxBufferSize = 8*1024

	def run(self):

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

	def ValidateFile(self, filePath):
		directory, fileName = os.path.split(filePath)
		if not os.path.exists(directory):
			os.makedirs(directory)

