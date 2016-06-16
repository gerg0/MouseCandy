#!/usr/bin/python2
import mcgi, mclass
import cgi
import pickle
import os

import cgitb
cgitb.enable()

form = cgi.FieldStorage()
file_to_load = form.getvalue("load")

file = open("templates/"+file_to_load, 'rb')
project = pickle.load(file)
file.close()

mcgi.frame()

print '<fieldset><legend>Project parameters</legend>'
print project.html()
print '</fieldset>'

if os.path.isfile("run/project.mcp"):
	print "<br>"
	mcgi.dummy_button("Start conditioning")
	print "<br>A project is already in progress."
else:
	start_form = mcgi.Form("start.py", buttontext="Start conditioning")
	start_form.addArgPass("running/project.mcp", "filename")
	project.passArgs(start_form)
	start_form.display()
