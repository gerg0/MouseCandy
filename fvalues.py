#!/usr/bin/python2
import cgi
import mcgi, mtools

noises = ["whitenoise", "pinknoise", "brownnoise", "tpdfnoise"]
form = cgi.FieldStorage()

def getInt(name):
	return mtools.toInt(form.getvalue(name))
	
def getFloat(name):
	return mtools.toFloat(form.getvalue(name))	

def getStr(name):
	return form.getvalue(name)

#Project
ptype = getStr("ptype")
name = getStr("name")
notes = getStr("notes")
video = getStr("video")

#PAV & GNG
stim_type = getStr("stim_type")
action_count = getInt("action_count")
stim_length = getFloat("stim_length")

#PAV
wait_time_min = getFloat("wait_time_min")
wait_time_max = getFloat("wait_time_max")

#GNG
positive_count = getInt("positive_count")

active_period = getFloat("active_period")
grace_preiod = getFloat("grace_period")
idle_period = getFloat("idle_period")

extra_time = getFloat("extra_time")
reset_on_random = getStr("reset_on_random")

#Olfactory General
blank_valve = getStr("blank_valve")

#Olfactory PAV
odor_valve_name = getStr("odor_valve_name")

#Olfactory GNG
positive_valve = getStr("positive_valve")
negative_valve = getStr("negative_valve")

#Audio PAV
tone_type = getStr("tone_type")

if tone_type in noises: 
	tone_hz = 0
else:
	tone_hz = getFloat("tone_hz")

#Audio GNG
positive_tone_type = form.getvalue("positive_tone_type")
negative_tone_type = form.getvalue("negative_tone_type")

if positive_tone_type in noises:
	positive_tone_hz = 0
else:
	positive_tone_hz = getInt("positive_tone_hz")

if negative_tone_type in noises:
	negative_tone_hz = 0
else:
	negative_tone_hz = getInt("negative_tone_hz")

#Visual General
line_width = getInt("line_width")
line_speed = getInt("line_speed")

#Visual PAV 
animation_angle = getFloat("animation_angle")

#Visual GNG
positive_animation = getFloat("positive_animation")
negative_animation = getFloat("negative_animation")

#Get filename for saving
filename = getStr("filename")
