import threading
import argparse
import os
import sys

class Command:
	def action(self):
		pass

class DefaultCommand(Command):
	def __init__(self, param):
		self.param = param
		
	def action(self):
		print ("Not recoginized command")


class PushCommand(Command):
	def __init__(self, param):
		self.param = param

	def action(self):
		print ("This is Push command")

class FetchCommand(Command):
	def __init__(self, param):
		self.param = param

	def action(self):
		print ("This is Fetch command")

class HelpCommand(Command):
	def action(self):
		print ('This is a utility to transfer file between server and client' + os.linesep + "usage:\t<push|fetch|exit|help> [-v] [-m MACHINE_NAME] [-s SOURCE_FILE] [-d DEST_FILE]")

class ExitCommand(Command):
	def action(self):
		sys.stdout.write("Bye!")
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
