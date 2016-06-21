#!/usr/bin/python2
import mcgi, mclass
import cgi
import cgitb
import os
import time
import pickle
cgitb.enable()

class Template(object):
	def __init__(self, filename):
		
		self.filename = filename
		
		self.ctime_str = time.ctime(os.path.getctime("templates/"+filename))	#Gets file creation time to a standard string
		self.ctime = time.strptime(self.ctime_str)								#Convers string to stucture	
		
		self.ctime_date = time.strftime("%Y.%m.%d.", self.ctime)				#Gets formatted date
		self.ctime_time = time.strftime("%H:%M:%S", self.ctime)					#Gets formatted time
		
		file = open("templates/"+filename, 'rb')
		project = pickle.load(file)
		file.close()
		
		self.name = project.name
		self.tags = str(project).split("\n")
		self.tags = self.tags[0]

	def html(self):
		print ('<tr>')
		print ('<td>' + mcgi.quickCheckbox(self.filename) + '</td>')
		print ('<td><a href="load_project.py?load='+self.filename+'">'+self.name+'</a></td>')
		print ('<td>'+self.tags+'</td>')
		print ('<td>'+self.ctime_date+'</td>')
		print ('<td>'+self.ctime_time+'</td>')
		print ('<td><a href="templates/'+self.filename+'" download>'+self.filename+'</a></td>')
		print ('</tr>')

mcgi.frame()
form = cgi.FieldStorage()
for templatefile in os.listdir("templates/"): 
	if form.getvalue(templatefile) == "del":
		print ('<p>'+templatefile+" deleted</p>")
		os.remove("templates/"+templatefile)


templatefiles = []
for filename in os.listdir("templates/"): templatefiles.append(Template(filename))
def getkey(custom): return custom.ctime
templatefiles = sorted(templatefiles, key=getkey, reverse=True)

print('<form action="templates.py" method="post">')


print ('<table style="width:90%">')
print ('<tr>')
print ('<td><b>   </b></td>')
print ('<td><b>Name</b></td>')
print ('<td><b>Tags</b></td>')
print ('<td><b>Date</b></td>')
print ('<td><b>Time</b></td>')
print ('<td><b>Download</b></td>')
print ('</tr>')
for template in templatefiles: template.html()
print ('</table>')

print ('<br>')

print '<input type="submit" value="Delete selected">'
print '</form>'

print('</body></html>')
