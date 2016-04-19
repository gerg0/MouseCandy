#!/usr/bin/python2
import mcgi, mclass
import fvalues
import pickle
import pmaker

mcgi.frame()
p = pmaker.make_project()

print ('<h4>Project saved as "'+fvalues.filename+'.mcp"</h4>')
print '<fieldset><legend>Project parameters</legend>'

print p.html()

print '</fieldset>'

file = open("templates/"+fvalues.filename+".mcp", 'wb')
pickle.dump(p, file)
file.close()
