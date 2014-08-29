import os
import sys
from socket import *
from struct import *
from Task import *

class ServerReceiveTask(Task):
	def __init__(self, socket, address):
		self.socket = socket
		self.address = address
		self.bufferSize = 8*1024
		#print ("init a ServerReceiveTask")

	def run(self):
		#print("start to receive data")

		while True:
			headLength = calcsize('!128sI')
			head = self.socket.recv(headLength)
			fileName, fileSize = unpack('!128sI', head)
			fileName = fileName.strip('\00')
			#print('filename and size is %s %d' % (fileName,fileSize))

			self.ValidateFile(fileName)
			file = open(fileName, 'wb')
			if fileSize == 0:
				file.close()
				continue

			receiveSize = 0
			while(True):
				body = self.socket.recv(self.bufferSize)
				#print('body is %s' % body)

				file.write(body)
				receiveSize += len(body)
				#print('%d of %d byes of data are received' % (receiveSize,fileSize))
				if receiveSize == fileSize:
					file.close()
					break
				
			self.socket.close()
			break

	def ValidateFile(self, filePath):
		directory, fileName = os.path.split(filePath)
		if not os.path.exists(directory):
			os.makedirs(directory)

