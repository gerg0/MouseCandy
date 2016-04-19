from time import time
from math import sqrt

def toInt(var):
	try:
		return int(var)
	except Exception:
		return None
		
def toFloat(var):
	try:
		return float(var)
	except Exception:
		return None

def toString(var, padded = True):
	if padded:
		return "%12.6f" %var
	else:
		return "%.6f" %var

def avg(data):
	return sum(data)/len(data)
	
def dev(data):
	return sqrt(sum(map(lambda a: (avg(data)-a)**2, data))/len(data))


	
class Stopwatch(object):
	def __init__(self):
		self.start_time = time()
		
	def __str__(self):	
		return "%12.6f sec" %(time()-self.start_time)
		
	def value(self):
		return time()-self.start_time
		
	def reset(self):
		self.start_time = time()
		
class Timer(object):
	def __init__(self, length=0):
		self.length = length
		self.until = time()+self.length
	
	def __str__(self):
		return "%12.6f sec" %(self.until-time())
		
	def is_running(self):
		return time() < self.until
	
	def set(self, length):
		self.length = length
		
	def reset(self):
		self.until = time()+self.length
