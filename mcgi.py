#!/usr/bin/python2
import cgi
import cgitb
import Cookie
cgitb.enable()
import os
	

#print cookie.output()
#Set-Cookie: theme=light

pwd = os.getcwd()

def show(file):
	with open('gui/'+file, 'r') as fin:
	    print fin.read()

def passarg(var, name):
	#Pass arguments with this
	print('<input type="hidden" name='+name+' value="'+var+'">')	
	
def conditioning():
	print('<body>')
	print("<center><h2>Conditioning in progress...</h2	></center>")	
	print('<center><img src="/giphy.gif"></center>')

	print('</body>')

def frame():
	print("Content-type:text/html\r\n\r\n")
	try:
		cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
		theme = cookie["theme"].value
		print ('<link rel="stylesheet" href="/css/'+theme+'.css" >')
	except (Cookie.CookieError, KeyError):
		print('<link rel="stylesheet" href="/css/solarized-light.css" >')
	show("frame.html")

def link(text, url, target="_self", paragraph=True):
	if paragraph:
		print '<p><a href="'+url+'" target='+target+'>'+text+'</a></p>'
	else:
		print '<a href="'+url+'" target='+target+'>'+text+'</a>'
		
def start_button(project):
	start_form = Form("start.py", buttontext="Start conditioning")
	start_form.addArgPass("running/project", "filename")
	project.passArgs(start_form)
	start_form.display()

def save_button(project):
	save_temp_form = Form("save_template.py", buttontext="Save as template")
	save_temp_form.addInput("Filename","filename", unit=".mcp", value=project.name)
	project.passArgs(save_temp_form)
	save_temp_form.display()

def dummy_button(text):
	print '<button type="button" disabled>'+text+'</button>'

def quickCheckbox(name, value="del"):
	return ('<input type="checkbox" name="'+name+'" value="'+value+'">')

class Form(list):
	def __init__(self, action, method="post", buttontext="Next"):
		super(list,self).__init__()
		self.action = action
		self.method = method
		self.buttontext = buttontext

	def display(self):
		print('<form action="'+self.action+'" method="'+self.method+'">')
		for element in self: print element
		print '<input type="submit" value="'+self.buttontext+'">'
		print '</form>'
		
	def addInput(self, title, name, inputtype="text", size="15", value="", hint="", warning="", unit="", close_paragraph=True):
		if type(size) is not str: size = str(size)
		if hint != "": hint = '<br><i>' +hint+ '</i>'
		if warning != "": warning = '<font color="red"> '+warning+'</font>'
		if title != "": title = title + '<br>'
		
		if close_paragraph:
			self.append('<p>'+title+' <input type="'+inputtype+'" name="'+name+'" size="'+size+'" value="'+str(value)+'"> '+unit+warning+hint+'</p>')
		else:
			self.append('<p>'+title+' <input type="'+inputtype+'" name="'+name+'" size="'+size+'" value="'+str(value)+'"> '+unit+warning+hint)
	
	def addArgPass(self, value, name):
		self.addInput(title="", inputtype="hidden", value=value, name=name)
		
	def addTextarea(self, title, name, rows="10", cols="30", value=""):
		if type(rows) is not str: rows = str(rows)
		if type(cols) is not str: cols = str(cols)
		self.append('<p>'+title+' <br> <textarea name="'+name+'" rows="'+rows+'" cols="'+cols+'" >'+str(value)+'</textarea></p>')
	
	def addRadio(self, radio):
		self.append(radio)	
	
	def addLabel(self, text):
		self.append(text)
	
	class Radio(list):
		def __init__(self, title, name, hint=""):
			super(list,self).__init__()
			self.title = title
			self.name = name
			if hint != "": 
				self.hint = '<br><i>' +hint+ '</i>'
			else:
				self.hint = hint
		
		def __str__(self):
			return '<p>'+self.title+'<br>\n'+('\n'.join(self))+self.hint+'</p>'
			#return '<p>'+self.title+'<br><select name="'+self.name+'">'+'\n'+'\n'.join(self)+'</select></p>'
		
		def addOption(self, title, value, checked):
			if checked:
				checked = "checked"
			else:
				checked = ""
			self.append('<input type="radio" name="'+self.name+'" value="'+value+'" '+checked+'> '+title)
	
	def addSelect(self, select):
		self.append(select)
	
	class Select(list):
		def __init__(self, title, name, unit=""):
			super(list,self).__init__()
			self.title = title
			self.name = name
			self.unit = unit
			
		def __str__(self):
			if self.title == "":
				return '<select name="'+self.name+'">'+'\n'+'\n'.join(self)+'</select> '+self.unit+'</p>'
			else:
				return '<p>'+self.title+'<br><select name="'+self.name+'">'+'\n'+'\n'.join(self)+'</select> '+self.unit+'</p>'
		
		def addOption(self, text, value, selected=False):
			if selected:
				selected = ' selected="selected"'
			else:
				selected = ""
				
			self.append('<option value="'+value+'"'+selected+'">'+text+'</option>')
			
	def addCheckbox(self, title, name, value="on", checked=False, hint=""):
		if hint != "": hint = '<br><i>' +hint+ '</i>'
		if checked: 
			checked = "checked"
		else:
			checked = ""
		self.append('<p><input type="checkbox" name="'+name+'" value="'+value+'" '+checked+'> '+title+hint+'</p>')
		

