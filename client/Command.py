import os,sys,argparse,threading
from ClientSendTask import *
from ClientReceiveTask import *


class Command:
	def __init__(self, param):
		pass

	def action(self):
		pass

class DefaultCommand(Command):
	def __init__(self, param):
		self.param = param
		
	def action(self):
		print ("Not recoginized command")
		return None


class PushCommand(Command):
	def __init__(self, param):
		self.param = param

	def action(self):
		task = ClientSendTask(self.param.host, self.param.port)
		task.SetSourAndDestDir(self.param.sourDir, self.param.destDir)
		return task

class FetchCommand(Command):
	def __init__(self, param):
		self.param = param

	def action(self):
		task = ClientReceiveTask(self.param.host, self.param.port)
		task.SetSourAndDestDir(self.param.sourDir, self.param.destDir)
		return task

class HelpCommand(Command):
	def __init__(self):
		pass

	def action(self):
		print ('This is a utility to transfer file between server and client' + os.linesep + "usage:\t<push|fetch|exit|help> [-v] [-m MACHINE_NAME] [-s SOURCE_FILE] [-d DEST_FILE]")
		return None

class ExitCommand(Command):
	def __init__(self):
		pass

	def action(self):
		print("Bye!")
		sys.exit(0)

class CommandFactory:
	def createCommand(self, param):
		if param.name == "push":
			return PushCommand(param)
		elif param.name == "fetch":
			return FetchCommand(param)
		elif param.name == "help":
			return HelpCommand()
		elif param.name == "exit":
			return ExitCommand()
		else:
			return DefaultCommand(param)
