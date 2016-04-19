#!/usr/bin/python2
import mcgi, mclass
import cgi
import cgitb
import os
import time
import pickle
cgitb.enable()

mcgi.frame()
#print ('<h4><font color="red">Work in progress. This site is just a placeholder.</font></h4>')
print("<h4>Menage saved projects.</h4><br>")

print ('<table style="width:70%">')
print ('<tr>')
print ('<td><b>Name</b></td>')
print ('<td><b>Date</b></td>')
print ('<td><b>Time</b></td>')
print ('<td><b>Download</b></td>')
print ('</tr>')
for filename in sorted(os.listdir("templates/")):
	file = open("templates/"+filename, 'rb')
	project = pickle.load(file)
	file.close()
	
	ctime_str = time.ctime(os.path.getctime("templates/"+filename))					#Gets file creation time to a standard string
	ctime = time.strptime(ctime_str)												#Convers string to stucture
	ctime_date = time.strftime("%Y.%m.%d.", ctime)									#Gets formatted date
	ctime_time = time.strftime("%H:%M:%S", ctime)									#Gets formatted time
	
	print ('<tr>')
	
	#print ('<td>'+project.name+'</td>')
	print ('<td>')
	mcgi.link(project.name, "load_project.py?load="+filename, paragraph=False)
	print ('</td>')
	
	print ('<td>'+ctime_date+'</td>')
	print ('<td>'+ctime_time+'</td>')
	print ('<td><a href='+'"templates/'+filename+'" download>'+filename+'</a></td>')
	
	print ('</tr>')

print ('</table>') 