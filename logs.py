#!/usr/bin/python2
import cgi
import cgitb
cgitb.enable()
import os
import time
import random
import mcgi

mcgi.frame()
#mcgi.show("frame.html")
#print ('<h4><font color="red">Work in progress. Logs are not implemented, this site is just a placeholder.</font></h4>')
print("<h4>Here you can find all the log files of previous projects.</h4><br>")

print ('<table style="width:70%">')
for filename in sorted(os.listdir("logs/")):
	ctime_str = time.ctime(os.path.getctime("logs/"+filename))	#Gets file creation time to a standard string
	ctime = time.strptime(ctime_str)												#Convers string to stucture
	ctime_date = time.strftime("%Y.%m.%d.", ctime)									#Gets formatted date
	ctime_time = time.strftime("%H:%M:%S", ctime)									#Gets formatted time
	print ('<tr>')
	print ('<td><a href='+'"logs/'+filename+'">'+filename+'</a></td>')
	print ('<td><a href='+'"	logs/'+filename+'" download>Download</a></td>')
	print ('<td>'+ctime_date+'</td>')
	print ('<td>'+ctime_time+'</td>')
	print ('</tr>')

print ('</table>')

print('</body></html>')


