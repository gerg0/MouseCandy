#!/usr/bin/python2
import mcgi, mclass
import fvalues
import pmaker
import os

mcgi.frame()

err = False

#Check for stim length error (generic)	
if fvalues.stim_length is None: err = True

#Check for GNG specific errors
if fvalues.ptype == "gng":
	#Check for OlfactoryGNG specific errors
	if fvalues.stim_type == "olfactory":
		if fvalues.positive_valve == fvalues.negative_valve: err = True
		if fvalues.positive_valve == fvalues.blank_valve: err = True
		if fvalues.negative_valve == fvalues.blank_valve: err = True
		
	#Check for AudioGNG specific errors
	if fvalues.stim_type == "audio":
		if fvalues.positive_tone_hz is None: err = True
		if fvalues.negative_tone_hz is None: err = True
		
	#Check for VisualGNG specific errors
	if fvalues.stim_type == "visual":
		if fvalues.positive_animation is None: err = True	
		if fvalues.negative_animation is None: err = True
		if fvalues.positive_animation == fvalues.negative_animation: err = True
		if fvalues.line_width is None: err = True
		if fvalues.line_speed is None: err = True

#Check for PAV specific errors
if fvalues.ptype == "pav":
	#Check for OlfactoryPAV specific errors
	if fvalues.stim_type == "olfactory":
		if fvalues.odor_valve_name == fvalues.blank_valve: err = True
		
	#Check for AudioPAV specific errors
	if fvalues.stim_type == "audio":
		if fvalues.tone_hz is None: err = True
	
	#Check for VisualPAV specific errors
	if fvalues.stim_type == "visual":
		if fvalues.animation_angle is None: err = True	
		if fvalues.line_width is None: err = True
		if fvalues.line_speed is None: err = True




#Display last form if there were any errors
if err:
	print ('<h4>Failed to move on...</h4>')

	#GNG parent due to error	
	if fvalues.ptype == "gng":
		p = mclass.Gng(fvalues.name, fvalues.notes, fvalues.video, \
			fvalues.action_count, fvalues.positive_count, fvalues.grace_preiod, fvalues.active_period, fvalues.idle_period, fvalues.extra_time, fvalues.reset_on_random)
		
		print '<fieldset><legend>Project parameters</legend>'
		print p.html()
		print '</fieldset>'	
		
		#OlfactoryGNG form due to error		
		if fvalues.stim_type == "olfactory": 
			mclass.OlfactoryGng.showForm(fvalues.positive_valve, fvalues.negative_valve, \
				fvalues.blank_valve, fvalues.stim_length, parent=p)
		
		#AudioGNG form due to error	
		if fvalues.stim_type == "audio": 
			mclass.AudioGng.showForm(fvalues.positive_tone_hz, fvalues.positive_tone_type, \
				fvalues.negative_tone_hz, fvalues.negative_tone_type, \
				fvalues.stim_length, parent=p)
		
		#VisualGNG form due to error			
		if fvalues.stim_type == "visual":
			mclass.VisualGng.showForm(fvalues.positive_animation, fvalues.negative_animation, \
				fvalues.line_width, fvalues.line_speed, fvalues.stim_length, parent=p)
				
	#PAV parent due to error																	
	if fvalues.ptype == "pav":		
		p = mclass.Pav(fvalues.name, fvalues.notes, fvalues.video, \
					fvalues.action_count, fvalues.wait_time_min, fvalues.wait_time_max)
					
		print '<fieldset><legend>Project parameters</legend>'
		print p.html()
		print '</fieldset>'	
			
		#OlfactoryPAV form due to error
		if fvalues.stim_type == "olfactory": mclass.OlfactoryPav.showForm(fvalues.odor_valve_name, fvalues.blank_valve, \
			fvalues.stim_length, parent=p)
		
		#AudioPAV form due to error	
		if fvalues.stim_type == "audio": mclass.AudioPav.showForm(fvalues.tone_hz, fvalues.tone_type, \
			fvalues.stim_length, parent=p)
																	
		#VisualPAV form due to error	
		if fvalues.stim_type == "visual": mclass.VisualPav.showForm(fvalues.animation_angle, fvalues.line_width, fvalues.line_speed, \
			fvalues.stim_length, parent=p)
																	
																													
#No errors. Finalize project																	
else:
	
	p = pmaker.make_project()
	
	print ('<h4>New project is ready.</h4>')
	
	print '<fieldset><legend>Project parameters</legend>'
	print p.html()
	print '</fieldset>'
	
	mcgi.save_button(p)
	print "<br>"
	
	if os.path.isfile("run/project"):
		mcgi.dummy_button("Start")
		print "<br><i>An other project is already running.</i>"
	else:
		mcgi.start_button(p)

