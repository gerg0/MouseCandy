from time import time
from math import sqrt
import binascii

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
	if data == []: 
		return 0
	else:
		return sum(data)/len(data)
	
def dev(data):
	if data == []: 
		return 0
	else: 
		return sqrt(sum(map(lambda a: (avg(data)-a)**2, data))/len(data))

def CRC32_from_file(filename):
    buf = open(filename,'rb').read()
    buf = (binascii.crc32(buf) & 0xFFFFFFFF)
    return "%08X" % buf
	
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
