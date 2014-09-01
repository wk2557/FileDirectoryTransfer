import threading
import argparse

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

class CommandFactory:
	def createCommand(self, param):
		if param.name == "push":
			return PushCommand(param)
		elif param.name == "fetch":
			return FetchCommand(param)
		else:
			return DefaultCommand(param)
