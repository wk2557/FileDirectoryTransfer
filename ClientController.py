import argparse
import platform
import sys
import os
import Command


class ClientController:
	def __init__(self):
		self.commandFactory = Command.CommandFactory()
		self.parser = argparse.ArgumentParser(description = 'This is a utility to transfer file between server and client', usage = "<push|fetch|exit|help> [-v] [-m MACHINE_NAME] [-s SOURCE_FILE] [-d DEST_FILE]")
		self.parser.add_argument('name', action = "store", help = "command name <push|fetch|exit|help>")
		self.parser.add_argument('-v', action = "store_true", dest = "verbose", help = "print the process log")
		self.parser.add_argument('-m', action = "store", dest = "mahcine_name", help = "dest machine")
		self.parser.add_argument('-s', action = "store", dest = "source_file",  help = "source file to transfer")
		self.parser.add_argument('-d', action = "store", dest = "dest_file", help = "dest file to transfer")

	def printPrompt(self):
		sys.stdout.write("$:")

	def printLine(self, string):
		sys.stdout.write(string)
		sys.stdout.write(os.linesep)

	def run(self):
		while True:
			try:
				self.printPrompt()
				cmdString = sys.stdin.readline()
				cmdString = cmdString.strip('\n')
				cmdList = cmdString.split(' ')
				command = self.commandFactory.createCommand(self.parser.parse_args(cmdList))
				command.action()
			except KeyboardInterrupt:
				sys.exit(0)
			except SystemExit:
				sys.exit(0)
			except:
				pass
			finally:
				pass

			


if __name__ == '__main__':
	cc = ClientController()
	cc.run()
	print "test"