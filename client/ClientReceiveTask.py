from socket import *
from struct import *
import os
import sys

class FileTransferClient:
	def __init__(self, portNum, host):
		self.portNum = portNum
		self.host = host
		self.bufferSize = 8 * 1024
		self.socket = socket(AF_INET, SOCK_STREAM)		

	def Send(self, fileName, destPath):	
		#fileName = unicode(fileName, 'utf8')
		if not os.path.exists(fileName.decode('GBK')):
			print ("File: %s not exists" % fileName.decode("GBK"))
			sys.exit()

		self.socket.connect((self.host, self.portNum))	
		print ("begin to send file: %s" % fileName)
		head = pack('!128sI', destPath, os.stat(fileName).st_size)
		self.socket.send(head)
		file = open(fileName, 'rb')
		while True:
			date = file.read(self.bufferSize)
			if not date:
				break
			self.socket.send(date)
		print ("End of send file: %s" % fileName)
		file.close()
		self.socket.close()

def ParseDir(absDir, fatherDir, files):
		if os.path.isdir(absDir):
			listOfFiles = os.listdir(absDir)
			for theFile in listOfFiles:
				if os.path.isdir(absDir + os.path.sep + theFile):
					ParseDir(absDir + os.path.sep + theFile, fatherDir + os.path.sep + theFile, files)
				else:
					files.append(fatherDir + os.path.sep + theFile)


if __name__ == '__main__':
	if len(sys.argv) < 3:
		print ("not enough args, please input source, des-machine and des-path")
		sys.exit()

	port = 8973
	fileName = sys.argv[1]
	machineName = sys.argv[2]
	destPath = sys.argv[3]
	"""
	fileName = "D:\\code\\"
	DestPath = "D:\\test\\"
	
	machineName = "vcdbj-kuwang-3"
	"""
	files = []
	baseDir = ""
	if os.path.isdir(fileName):
		ParseDir(fileName, "", files)
		baseDir = fileName.strip(os.path.sep)
	else:
		dirs, name = os.path.split(fileName)
		files.append(name)
		baseDir = dirs
	print files
	
	for theFile in files:	
		client = FileTransferClient(port, machineName)
		client.Send(baseDir + theFile, destPath + theFile)
