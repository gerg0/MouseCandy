#!/usr/bin/python2
import mclass
import fvalues

def make_project():

	if fvalues.ptype == "gng":
		if fvalues.stim_type == "olfactory":
			p = mclass.OlfactoryGng(fvalues.name, fvalues.notes, fvalues.video, \
					fvalues.action_count, fvalues.positive_count, fvalues.grace_preiod, fvalues.active_period, fvalues.idle_period, fvalues.extra_time, fvalues.reset_on_random,\
					fvalues.positive_valve, fvalues.negative_valve, fvalues.blank_valve, fvalues.stim_length)
					
		if fvalues.stim_type == "audio":
			p = mclass.AudioGng(fvalues.name, fvalues.notes, fvalues.video, \
					fvalues.action_count, fvalues.positive_count, fvalues.grace_preiod, fvalues.active_period, fvalues.idle_period, fvalues.extra_time, fvalues.reset_on_random,\
					fvalues.positive_tone_hz, fvalues.positive_tone_type, fvalues.negative_tone_hz, fvalues.negative_tone_type, fvalues.stim_length)
	
	if fvalues.ptype == "pav":
		if fvalues.stim_type == "audio":
			p = mclass.AudioPav(fvalues.name, fvalues.notes, fvalues.video, \
					fvalues.action_count, fvalues.wait_time_min, fvalues.wait_time_max,	 \
					fvalues.tone_hz, fvalues.tone_type, fvalues.stim_length)	
	
	
	return p
