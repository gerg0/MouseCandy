#!/usr/bin/python2
import cgi
import cgitb
cgitb.enable()
import os
import time
import random
import mcgi

import zipfile

class Logfile(object):
	def __init__(self, filename):
		
		self.filename = filename
		
		self.ctime_str = time.ctime(os.path.getctime("logs/"+filename))	#Gets file creation time to a standard string
		self.ctime = time.strptime(self.ctime_str)						#Convers string to stucture	
		
		self.ctime_date = time.strftime("%Y.%m.%d.", self.ctime)		#Gets formatted date
		self.ctime_time = time.strftime("%H:%M:%S", self.ctime)			#Gets formatted time
		
		self.zipobject = zipfile.ZipFile("logs/"+filename, 'r')

	def html(self):
		print ('<tr>')
		print ('<td>' + mcgi.quickCheckbox(self.filename) + '</td>')
		print ('<td><a href='+'"logs/'+self.filename+'" download>'+self.filename+'</a></td>')
		print ('<td>'+self.zipobject.comment+'</td>')
		print ('<td>'+self.ctime_date+'</td>')
		print ('<td>'+self.ctime_time+'</td>')
		print ('</tr>')

mcgi.frame()

form = cgi.FieldStorage()
for logfile in os.listdir("logs/"): 
	if form.getvalue(logfile) == "del":
		print ('<p>'+logfile+" deleted</p>")
		os.remove("logs/"+logfile)


#mcgi.show("frame.html")
#print ('<h4><font color="red">Work in progress. Logs are not implemented, this site is just a placeholder.</font></h4>')
#print("<h4>Here you can find all the log files of previous projects.</h4><br>")


logfiles = []
for filename in os.listdir("logs/"): logfiles.append(Logfile(filename))
def getkey(custom): return custom.ctime
logfiles = sorted(logfiles, key=getkey, reverse=True)


print('<form action="logs.py" method="get">')


print ('<table style="width:99%">')
print ('<tr>')
print ('<td><b>   </b></td>')
print ('<td><b>File</b></td>')
print ('<td><b>Tags</b></td>')
print ('<td><b>Date</b></td>')
print ('<td><b>Time</b></td>')
print ('</tr>')
for logfile in logfiles: logfile.html()
print ('</table>')

print ('<br>')

print '<input type="submit" value="Delete selected">'
print '</form>'

print('</body></html>')


