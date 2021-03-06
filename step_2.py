#!/usr/bin/python2
import mcgi, mclass
import fvalues

mcgi.frame()

#Check for errors (Only possible error is an empty name field)
if fvalues.name is None:
	print ('<h4>Failed to move on...</h4>')
	mclass.Project.showForm(fvalues.name, fvalues.ptype, fvalues.notes, fvalues.video)
	
else:
	print ('<h4>Step 2/3</h4>')
	p = mclass.Project(fvalues.name, fvalues.notes, fvalues.video)
	print '<fieldset><legend>Project parameters</legend>'
	print p.html()
	print '</fieldset>'
	if fvalues.ptype == "gng": mclass.Gng.showForm(parent=p)
	if fvalues.ptype == "dsc": mclass.Dsc.showForm(parent=p)
	if fvalues.ptype == "pav": mclass.Pav.showForm(parent=p)
