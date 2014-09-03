import os, sys, argparse, platform

sys.path.append("./client")
sys.path.append("./common")

import Command
from socket import *
from Task import *
from ThreadManager import *

class ClientController:
	def __init__(self):
		self.parser = argparse.ArgumentParser(description = 'This is a utility to transfer file between server and client', usage = "<push|fetch|exit|help> [-v] [-m MACHINE_NAME] [-s SOURCE_FILE] [-d DEST_FILE]")
		self.parser.add_argument('name', action = "store", help = "command name <push|fetch|exit|help>")
		self.parser.add_argument('-v', action = "store_true", dest = "verbose", help = "print the process log")
		self.parser.add_argument('-m', action = "store", dest = "host", help = "destination host name")
		self.parser.add_argument('-p', action = "store", dest = "port", help = "the port of destination host")
		self.parser.add_argument('-s', action = "store", dest = "sourDir",  help = "source directory to transfer")
		self.parser.add_argument('-d', action = "store", dest = "destDir", help = "destination directory to store")
		
		self.commandFactory = Command.CommandFactory()
		self.taskManager = TaskManager(1)

	def run(self):
		while True:
			try:
				sys.stdout.write("$ ")
				sys.stdout.flush()
				cmdString = sys.stdin.readline()
				cmdString = cmdString.strip('\n')
				cmdList = cmdString.split(' ')

				parameter = self.parser.parse_args(cmdList)
				if parameter.host == None:
					parameter.host = '127.0.0.1'
				if parameter.port == None:
					parameter.port = 8973

				command = self.commandFactory.createCommand(parameter)
				task = command.action()
				if task != None:
					self.taskManager.insertTask(task)

			except KeyboardInterrupt:
				self.taskManager.setStop()
				print("keyboard interupt")
				sys.exit(0)

			except SystemExit:
				self.taskManager.setStop()
				sys.exit(0)

			finally:
				#self.taskManager.setStop()
				#print("finally")
				pass

			
if __name__ == '__main__':
	cc = ClientController()
	cc.run()
	print("test")

