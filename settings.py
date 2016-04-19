#!/usr/bin/python2
import cgi
import mcgi
import Cookie
import os

form = cgi.FieldStorage()
theme = form.getvalue("theme")
if theme is not None:
	cookie = Cookie.SimpleCookie()
	cookie["theme"] = theme
	#print("Content-type:text/html")
	print cookie.output()
	#print
else:
	#mcgi.ctype()
	if 'HTTP_COOKIE' in os.environ:
		cookie_string=os.environ.get('HTTP_COOKIE')
		c=Cookie.SimpleCookie()
		c.load(cookie_string)
	#cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
		try:
			theme = c["theme"].value
		except KeyError:
			#print "The cookie was not set or has expired<br>"
			theme="solarized-light"

mcgi.frame()	
#mcgi.show("frame.html")	

print('<form action="settings.py" method="post"> ')
print('<select name="theme"> ')

if theme=="solarized-light":
	print('<option value="solarized-light" selected>Solarized Light</option>' )
else:
	print('<option value="solarized-light">Solarized Light</option>' )

if theme=="solarized-dark":
	print('<option value="solarized-dark" selected>Solarized Dark</option> ')
else:
	print('<option value="solarized-dark">Solarized Dark</option> ')
	
print('</select> ')
print('<input type="submit" value="Save">')
print('</form>')
	
