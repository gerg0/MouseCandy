#This file contains a class for discrimination tasks. Could be implemented later.

class Dsc(Project):
	form = "dsc_form.html"
	def __init__(self, name, notes, video, \
			a_count, b_count, wait_time, on_stim_a):
			
		super(Dsc,self).__init__(name, notes, video)
 		self.a_count = a_count
		self.b_count = b_count
		self.stim_count = a_count + b_count
		self.wait_time = wait_time
		self.on_stim_a = on_stim_a
		self.on_stim_b = "sensor_B" if self.on_stim_a=="sensor_A" else "sensor_A"
	
	def __str__(self):
		return "[DSC] "+ super(Dsc,self).__str__() +\
			"\n#of 'A' stimuli: "+str(self.a_count) +\
			"\n#of 'B' stimuli: "+str(self.b_count) +\
			"\n#of stimuli: "+str(self.stim_count) +\
			"\nWait time for action: " + str(self.wait_time) +" sec"+\
			"\nExpected answer for stim. 'A': " + self.on_stim_a +\
			"\nExpected answer for stim. 'B': " + self.on_stim_b 
			
	def html(self):
		return super(Dsc,self).html() +\
			"<p>" +\
			"<b>Type: </b> Discrimination" +\
			"<br><b>#of 'A' stimuli: </b>"+str(self.a_count) +\
			"<br><b>#of 'B' stimuli: </b>"+str(self.b_count) +\
			"<br><b>#of stimuli: </b>"+str(self.stim_count) +\
			"<br><b>Wait time for action: </b>" + str(self.wait_time) +" sec"+\
			"<br><b>Expected answer for stim. 'A': </b>" + self.on_stim_a +\
			"<br><b>Expected answer for stim. 'B': </b>" + self.on_stim_b +\
			"</p>"

class OlfactoryDsc(Dsc):
	form = "olfactorydsc_form.html"
	def __init__(self, name, notes, video, \
			a_count, b_count, wait_time, on_stim_a,\
			a_valve, stim_length):
		
		super(OlfactoryDsc,self).__init__(name, notes, video, a_count, b_count, wait_time, on_stim_a)
		self.a_valve = a_valve
		self.b_valve = "vB" if self.a_valve=="vA" else "vA"
		self.stim_length = stim_length
		
	def __str__(self):
		return "[Olfactory] "+ super(OlfactoryDsc,self).__str__() +\
			"\nValve for fragrance 'A': "+self.a_valve +\
			"\nValve for fragrance 'B': "+self.b_valve +\
			"\nStim length: " + str(self.stim_length) +" sec"

	def html(self):
		return super(OlfactoryDsc,self).html() +\
			"<p>" +\
			"<b>Stimulus type: </b> Olfactory" +\
			"<br><b>Valve for fragrance 'A': </b>"+self.a_valve +\
			"<br><b>Valve for fragrance 'B': </b>"+self.b_valve +\
			"<br><b>Stim length: </b>" + str(self.stim_length) +" sec" +\
			"</p>"			
			
class AudioDsc(Dsc):
	form = "audiodsc_form.html"
	def __init__(self, name, notes, video, \
			a_count, b_count, wait_time, on_stim_a,\
			tone_a_hz, tone_a_type, tone_b_hz, tone_b_type, volume, stim_length):
		
		super(AudioDsc,self).__init__(name, notes, video, a_count, b_count, wait_time, on_stim_a)
		self.tone_a_hz = tone_a_hz	
		self.tone_a_type = tone_a_type
		self.tone_b_hz = tone_b_hz
		self.tone_b_type = tone_b_type
		self.volume = volume
		self.stim_length = stim_length
		
	def __str__(self):
		return "[Audio] "+ super(AudioDsc,self).__str__() +\
			"\nTone 'A': "+str(self.tone_a_hz) +" Hz "+self.tone_a_type+ " wave"+\
			"\nTone 'B': "+str(self.tone_b_hz) +" Hz "+self.tone_b_type+ " wave"+\
			"\nVolume: " + str(self.volume) +"%" +\
			"\nStim length: " + str(self.stim_length) +" sec"

	def html(self):
		return super(AudioDsc,self).html() +\
			"<p>" +\
			"<b>Stimulus type: </b> Audio" +\
			"<br><b>Tone 'A': </b>"+str(self.tone_a_hz) +" Hz "+self.tone_a_type+ " wave"+\
			"<br><b>Tone 'B': </b>"+str(self.tone_b_hz) +" Hz "+self.tone_b_type+ " wave"+\
			"<br><b>Volume: </b>" + str(self.volume) +"%" +\
			"<br><b>Stim length: </b>" + str(self.stim_length) +" sec" +\
			"</p>"
			
class VisualDsc(Dsc):
	form = "visualdsc_form.html"
	def __init__(self, name, notes, video, \
			a_count, b_count, wait_time, on_stim_a,\
			a_animation, stim_length):
		
		super(VisualDsc,self).__init__(name, notes, video, a_count, b_count, wait_time, on_stim_a)
		self.a_animation = a_animation
		self.b_animation = "horizontal" if self.a_animation=="vertical" else "vertical"
		self.stim_length = stim_length
		
	def __str__(self):
		return "[Visual] "+ super(VisualDsc,self).__str__() +\
			"\nAnimation for stim. 'A': "+self.a_animation +\
			"\nAnimation for stim. 'B': "+self.b_animation +\
			"\nStim length: " + str(self.stim_length) +" sec"

	def html(self):
		return super(VisualDsc,self).html() +\
			"<p>" +\
			"<b>Stimulus type: </b> Olfactory" +\
			"<br><b>Animation for stim. 'A': </b>"+self.a_animation +\
			"<br><b>Animation for stim. 'B': </b>"+self.b_animation +\
			"<br><b>Stim length: </b>" + str(self.stim_length) +" sec" +\
			"</p>"	
