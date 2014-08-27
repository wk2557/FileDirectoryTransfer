import os
import platform
from socket import *
from struct import *

class ServerStatusEnum:
	DISCONNECTED = 0
	LISTEN = 1
	READY = 2
	TRANSFER = 3

class FileTransferServerStatus:
	def BindAndListen(self, server):
		pass

	def Accpet(self, server):
		pass

	def ChangeStatus(self, server, serverStatus):
		server.ChangeStatus(serverStatus)


class FileTransferServerStatusDisconnected(FileTransferServerStatus):
	def __init__(self):
		self.value = ServerStatusEnum.DISCONNECTED

	def CreateSocket(self, server):
		assert server.status.value == ServerStatusEnum.DISCONNECTED
		status = FileTransferServerStatusListen()
		FileTransferServerStatus.ChangeStatus(self, server, status)

class FileTransferServerStatusListen(FileTransferServerStatus):
	def __init__(self):
		self.value = ServerStatusEnum.LISTEN

	def BindAndListen(self, server):
		assert server.status.value == ServerStatusEnum.LISTEN
		status = FileTransferServerStatusReady()
		FileTransferServerStatus.ChangeStatus(self, server, status)

class FileTransferServerStatusReady(FileTransferServerStatus):
	def __init__(self):
		self.value = ServerStatusEnum.READY

	def Accept(self, server):
		assert server.status.value == ServerStatusEnum.READY or server.status.value == ServerStatusEnum.TRANSFER
		status = FileTransferServerStatusTransfer()
		FileTransferServerStatus.ChangeStatus(self, server, status)

class FileTransferServerStatusTransfer(FileTransferServerStatus):
	def __init__(self):
		self.value = ServerStatusEnum.TRANSFER

	def Done(self, server):
		assert server.status.value == ServerStatusEnum.TRANSFER
		status = FileTransferServerStatusReady()
		FileTransferServerStatus.ChangeStatus(self, server, status)

class FileTransferServer:
	"Server"
	def __init__(self, portNum):
		self.portNum = portNum;
		self.status = FileTransferServerStatusDisconnected()
		self.socket = socket(AF_INET, SOCK_STREAM)
		self.status.CreateSocket(self)
		self.bufferSize = 1024 * 8

	def ChangeStatus(self, status):
		self.status = status

	def BindAndListen(self):
		self.socket.bind(('', self.portNum))
		self.socket.listen(5000)
		self.status.BindAndListen(self)
		
	def Work(self):

		while True:
			client,addr = self.socket.accept()
			while True:
				# if it is a new file, we first get the file name and file size
				if self.status.value == ServerStatusEnum.READY:
					headLength = calcsize('!128sI')
					head = client.recv(headLength)
					self.fileName, self.fileSize = unpack('!128sI', head)
					self.receiveSize = 0
					self.fileName = self.fileName.strip('\00')
					print ("Request from %s, file Name: %s, file Size: %d" % (str(addr), self.fileName, self.fileSize))
					self.status.Accept(server)
					self.ValidateFile(self.fileName)
					self.file = open(self.fileName, 'wb')
					if self.fileSize == 0:
						self.file.close()
						self.status.Done(server)
						print ("File %s receive successfully" % self.fileName)
						break
				else:
					print ("receive data")
					body = client.recv(self.bufferSize)
					self.file.write(body)
					self.receiveSize += len(body)
					if self.receiveSize == self.fileSize:
						self.file.close()
						self.status.Done(server)
						print ("File %s receive successfully" % self.fileName)
						break

	def ValidateFile(self, filePath):
		dirs, fileName = os.path.split(filePath)
		if not os.path.exists(dirs):
			os.makedirs(dirs)


if __name__ == '__main__':
	server = FileTransferServer(8973)
	server.BindAndListen()
	server.Work()
