#!/usr/bin/python2
import mcgi, mclass
import fvalues


mcgi.frame()


print ('<h4>Step 1/3</h4>')
mclass.Project.showForm()

"""
print('<form action="step_2.py" method="post">')
print mclass.Project.form(name=fvalues.name, type=fvalues.type, notes=fvalues.notes, video=fvalues.video)
fvalues.passOthers(this="project")
print('</form>')
"""