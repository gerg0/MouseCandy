#!/usr/bin/python2
import mcgi, mclass
import fvalues
import pickle
import pmaker

mcgi.frame()
p = pmaker.make_project()

print ('<p><h4>Project "'+fvalues.name+'" is ready to start</h4></p>')
print ('<p><h5>Confirm the project on the device</h5></p>')
print '<fieldset><legend>Project parameters</legend>'

print p.html()

print '</fieldset>'

file = open("run/project.mcp", 'wb')
pickle.dump(p, file)
file.close()
