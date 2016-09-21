#!/usr/bin/python2
import mcgi, mclass
import os
import pickle

mcgi.frame()
if os.path.isfile("/MouseCandy/run/project.mcp"):
	
	file = open("/MouseCandy/run/project.mcp", "rb")
	project = pickle.load(file)
	file.close()
	
	print('<h3>Project "'+project.name+'" is in progress...</h3>')	
	#print('<center><img src="/gui/giphy.gif"></center>')
	#print "<br>"
	
	print '<fieldset><legend>Project parameters</legend>'
	print project.html()
	print '</fieldset>'
	mcgi.link("New project", "step_1.py")

else:
	print("<h4>No conditioning in progress. Start one below.</h4>")
	mcgi.link("New project", "step_1.py")
	mcgi.link("Load project from template", "templates.py")
#mcgi.show("start.html")
