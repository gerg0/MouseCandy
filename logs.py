#!/usr/bin/python2
import cgi
import cgitb
cgitb.enable()
import os
import time
import random
import mcgi

class Logfile(object):
	def __init__(self, filename):
		
		self.filename = filename
		
		self.ctime_str = time.ctime(os.path.getctime("logs/"+filename))	#Gets file creation time to a standard string
		self.ctime = time.strptime(self.ctime_str)						#Convers string to stucture	
		
		self.ctime_date = time.strftime("%Y.%m.%d.", self.ctime)		#Gets formatted date
		self.ctime_time = time.strftime("%H:%M:%S", self.ctime)			#Gets formatted time

	def html(self):
		print ('<tr>')
		print ('<td><a href='+'"logs/'+self.filename+'" download>'+self.filename+'</a></td>')
		print ('<td>'+self.ctime_date+'</td>')
		print ('<td>'+self.ctime_time+'</td>')
		print ('</tr>')

mcgi.frame()
#mcgi.show("frame.html")
#print ('<h4><font color="red">Work in progress. Logs are not implemented, this site is just a placeholder.</font></h4>')
#print("<h4>Here you can find all the log files of previous projects.</h4><br>")


logfiles = []
for filename in os.listdir("logs/"): logfiles.append(Logfile(filename))
def getkey(custom): return custom.ctime
logfiles = sorted(logfiles, key=getkey, reverse=True)

print ('<table style="width:70%">')
for logfile in logfiles: logfile.html()
print ('</table>')

print('</body></html>')


