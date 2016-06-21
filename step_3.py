#!/usr/bin/python2
import mcgi, mclass
import fvalues

mcgi.frame()

err = False

#Check for GNG specific errors
if fvalues.ptype == "gng":
	if (fvalues.action_count is None) or (fvalues.positive_count is None): 
		err = True
	else:
		if int(fvalues.positive_count) > int(fvalues.action_count): err = True
		
	if fvalues.grace_preiod is None: err = True
	if fvalues.active_period is None: err = True
	if fvalues.idle_period is None: err = True
	
	if fvalues.extra_time is None: err = True
	if fvalues.grace_preiod is None: err = True

#Check for PAV specific errors
if fvalues.ptype == "pav":
	if fvalues.action_count is None: err = True
	if fvalues.wait_time_min is None: err = True
	if fvalues.wait_time_max is None: err = True
	
	
#Display last form if there were any errors
if err:
	print ('<h4>Failed to move on...</h4>')
	p = mclass.Project(fvalues.name, fvalues.notes, fvalues.video)	
	print '<fieldset><legend>Project parameters</legend>'
	print p.html()
	print '</fieldset>'
	
	#GNG form due to error	
	if fvalues.ptype == "gng":
		mclass.Gng.showForm(stim_type=fvalues.stim_type, \
							action_count=fvalues.action_count, \
							positive_count=fvalues.positive_count, \
							grace_preiod=fvalues.grace_period, \
							active_period=fvalues.active_period, \
							idle_period=fvalues.idle_period, \
							extra_time=fvalues.extra_time, \
							reset_on_random=fvalues.reset_on_random	, \
							parent=p)
	
	#PAV form due to error						
	if fvalues.ptype == "pav":
		mclass.Pav.showForm(stim_type=fvalues.stim_type, \
							action_count=fvalues.action_count, \
							wait_time_min=fvalues.wait_time_min,\
							wait_time_max=fvalues.wait_time_max,\
							parent=p)

#No errors. Display third form	
else:
	print ('<h4>Step 3/3</h4>')
	
	#GNG object
	if fvalues.ptype == "gng":
		p = mclass.Gng(fvalues.name, fvalues.notes, fvalues.video, \
				fvalues.action_count, fvalues.positive_count, \
				fvalues.grace_preiod, fvalues.active_period, fvalues.idle_period, \
				fvalues.extra_time, fvalues.reset_on_random)

	#PAV object
	if fvalues.ptype == "pav":
		p = mclass.Pav(fvalues.name, fvalues.notes, fvalues.video, \
				fvalues.action_count, fvalues.wait_time_min, fvalues.wait_time_max)
	
	#Display info sofar		
	print '<fieldset><legend>Project parameters</legend>'
	print p.html()
	print '</fieldset>'
	
	if fvalues.ptype == "gng":
		if fvalues.stim_type == "olfactory": mclass.OlfactoryGng.showForm(parent=p)
		if fvalues.stim_type == "audio": mclass.AudioGng.showForm(parent=p)
		if fvalues.stim_type == "visual": mclass.VisualGng.showForm(parent=p)
	
	if fvalues.ptype == "pav":
		if fvalues.stim_type == "olfactory": mclass.OlfactoryPav.showForm(parent=p)
		if fvalues.stim_type == "audio": mclass.AudioPav.showForm(parent=p)
		if fvalues.stim_type == "visual": mclass.VisualPav.showForm(parent=p)
