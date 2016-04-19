#!/usr/bin/python2
import cgi
import mcgi, mtools

noises = ["whitenoise", "pinknoise", "brownnoise", "tpdfnoise"]

form = cgi.FieldStorage()

#Get generic project settings
ptype = form.getvalue("ptype")
name = form.getvalue("name")
notes = form.getvalue("notes")
video = form.getvalue("video")

#Get PAV relevant settings
wait_time_min = form.getvalue("wait_time_min")
wait_time_min = mtools.toFloat(wait_time_min)

wait_time_max = form.getvalue("wait_time_max")
wait_time_max = mtools.toFloat(wait_time_max)

#PAV & GNG
stim_type = form.getvalue("stim_type")

action_count = form.getvalue("action_count")
action_count = mtools.toInt(action_count)

#Get GNG relevant settings	
positive_count = form.getvalue("positive_count")
positive_count = mtools.toInt(positive_count)

active_period = form.getvalue("active_period")
active_period = mtools.toFloat(active_period)
	
grace_preiod = form.getvalue("grace_preiod")
grace_preiod = mtools.toFloat(grace_preiod)

idle_period = form.getvalue("idle_period")
idle_period = mtools.toFloat(idle_period)

extra_time = form.getvalue("extra_time")
extra_time = mtools.toFloat(extra_time)

reset_on_random = form.getvalue("reset_on_random")


#Get Audio PAV relevant settings
tone_type = form.getvalue("tone_type")

if tone_type in noises: 
	tone_hz = 0
else:
	tone_hz = form.getvalue("tone_hz")
	tone_hz = mtools.toInt(tone_hz)

#Get Olfactory relevant settings
blank_valve = form.getvalue("blank_valve")

#Get Olfactory GNG relevant settings
positive_valve = form.getvalue("positive_valve")
negative_valve = form.getvalue("negative_valve")

#Get Audio GNG relevant settings
positive_tone_type = form.getvalue("positive_tone_type")
negative_tone_type = form.getvalue("negative_tone_type")


if positive_tone_type in noises:
	positive_tone_hz = 0
else:
	positive_tone_hz = form.getvalue("positive_tone_hz")
	positive_tone_hz = mtools.toInt(positive_tone_hz)

if negative_tone_type in noises:
	negative_tone_hz = 0
else:
	negative_tone_hz = form.getvalue("negative_tone_hz")
	negative_tone_hz = mtools.toInt(negative_tone_hz)



#volume = form.getvalue("volume")

#Get Visual GNG relevant settings
positive_animation = form.getvalue("positive_animation")

#Get Lenght. Relevant for all conditioning projects
stim_length = form.getvalue("stim_length")
stim_length = mtools.toFloat(stim_length)

#Get filename for saving
filename = form.getvalue("filename")

"""OBSELETE
def passOthers(this):

	if this != "project":
		#Pass project settings if they exist
		if type is not None: mcgi.passarg(type, "type")
		if name is not None: mcgi.passarg(name, "name")
		if notes is not None: mcgi.passarg(notes, "notes")
		if video is not None: mcgi.passarg(video, "video")
	
	if this != "gng":
		#Pass GNG settings if they exist
		if stim_type is not None: mcgi.passarg(stim_type, "stim_type")
		if action_count is not None: mcgi.passarg(action_count, "action_count")
		if positive_count is not None: mcgi.passarg(positive_count, "positive_count")
		if default_time is not None: mcgi.passarg(default_time, "default_time")
		if extra_time is not None: mcgi.passarg(extra_time, "extra_time")
		if random_extra_time is not None: mcgi.passarg(random_extra_time, "random_extra_time")
	
	if this != "olfactorygng":
		#Pass OlfactoryGNG settings if they exist
		if positive_valve is not None: mcgi.passarg(positive_valve,"positive_valve")

	if this != "audiogng":
		#Pass AudioGNG settings if they exist	
		if positive_tone_hz is not None: mcgi.passarg(positive_tone_hz, "positive_tone_hz")
		if positive_tone_type is not None: mcgi.passarg(positive_tone_type, "positive_tone_type")
		if negative_tone_hz is not None: mcgi.passarg(negative_tone_hz, "negative_tone_hz")
		if negative_tone_type is not None: mcgi.passarg(negative_tone_type, "negative_tone_type")
		if volume is not None: mcgi.passarg(volume, "volume")
	
	if this != "visualgng":
		#Pass VisualGNG settings if they exist	
		if positive_animation is not None: mcgi.passarg(positive_animation,"positive_animation")
	
	if (this != "olfactorygng") and (this != "audiogng") and (this != "visualgng"):
		#Pass length if it exists
		if length is not None: mcgi.passarg(length, "length")	
"""
