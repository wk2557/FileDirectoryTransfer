import threading
import time
from task import *

MAX_THREAD_NUM = 100

class MyQueue:
	def __init__(self):
		self.container = []

	def enqueue(self, item):
		self.container.append(item)

	def dequeue(self):
		if len(self.container) == 0:
			return None
		return self.container.pop(0)

	def size(self):
		return len(self.container)




class TaskManager:
	def __init__(self, threadNum = MAX_THREAD_NUM):
		self.max_thread_num = threadNum
		self.waitingListMutex = threading.Lock()
		self.waitingList = MyQueue()
		self.threadProxies = []
		self.stop = False
		for i in range (self.max_thread_num):
			self.threadProxies.append(ThreadProxy(self))

	def insertTask(self, task):
		self.waitingListMutex.acquire()
		self.waitingList.enqueue(task)
		print ("insert, len is %d" % self.waitingList.size())
		self.waitingListMutex.release()


	def pickUp(self):
		self.waitingListMutex.acquire()
		picked = self.waitingList.dequeue()
		print ("pickUp, len is %d" % self.waitingList.size())
		self.waitingListMutex.release()
		return picked

	def setStop(self):
		self.stop = True
		for item in self.threadProxies:
			item.join()

class ThreadProxy(threading.Thread):
	def __init__(self, tm):
		threading.Thread.__init__(self)
		self.taskManager = tm
		self.start()

	def run(self):
		while not self.taskManager.stop:
			picked = self.taskManager.pickUp()
			if picked != None:
				picked.run()


class TestTask(Task):
	def run(self):
		time.sleep(10)


if __name__ == '__main__':
	tm = TaskManager(50)
	starttime = time.clock()

	for i in range(50):
		t = TestTask();
		tm.insertTask(t)


	tm.setStop()
	endtime = time.clock()
	print (endtime - starttime)
	

