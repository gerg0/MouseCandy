import mcgi
import mtools
from mconfig import waves

class Project(object):	
	def __init__(self, name, notes, video):
		self.name = name
		if notes is None:
			self.notes = ""
		else:
			self.notes = notes
		
		if video == "on" :
			self.video = "on"
		else:
			self.video = "off"
		self.stim_length = 1
				
	def __str__(self):
		return "[Project]  "+\
			"\nName: "+self.name+\
			"\nNotes: "+self.notes+\
			"\nVideo: "+str(self.video)

	def html(self):
		return "<p>" +\
			"<b>Name: </b>" + self.name +\
			"<br><b>Notes: </b>" + self.notes +\
			"<br><b>Video: </b>" + self.video +\
			"</p>"
	
	def passArgs(self, form):	
		form.addArgPass(self.name, "name")
		form.addArgPass(self.notes, "notes")
		form.addArgPass(self.video, "video")

	def run(self):
		import mvalve, mconfig, msensor
		from progressbar import progress
	
		mconfig.GPIO_init()
		
		#Setup timers and stopwatches
		self.since_start = mtools.Stopwatch()
		self.since_stim = mtools.Stopwatch()
		self.stim_timer = mtools.Timer(self.stim_length)
		self.main_timer = mtools.Timer()
		
		self.water_valve = mvalve.Valve(pin = mconfig.drink_pin, pulse_length = mconfig.drink_time)
		self.sensor = msensor.Sensor(mconfig.sensor_pin)
		self.log = []
		
		import Adafruit_CharLCD as LCD
		#Initialize the LCD using the pins 
		lcd = LCD.Adafruit_CharLCDPlate()

		#Display project name & empty progressbar to LCD	
		lcd.home()
		lcd.message(self.name)
		progress(0)
		
	@staticmethod
	def showForm(name="", ptype="gng", notes="", video="off", err=""):
		if name is None: name = ""
		if ptype is None: ptype = ""
		if notes is None: notes = ""
		if video is None: video = ""
		
		f = mcgi.Form("step_2.py")

		typeselect = mcgi.Form.Select("Type","ptype")
		typeselect.addOption("Go/No-Go", "gng", selected=[False, True][ptype=="gng"])
		typeselect.addOption("Discrimination", "dsc", selected=[False, True][ptype=="dsc"])
		typeselect.addOption("Pavlovian", "pav", selected=[False, True][ptype=="pav"])

		f.addSelect(typeselect)

		if err == "noname":
			f.addInput("Name", "name", warning="Please name your project!")
		else:
			f.addInput("Name", "name", value=name)

		f.addTextarea("Notes", "notes", value=notes)
		if video == "on":
			f.addCheckbox("Record video", "video", checked=True)
		else:
			f.addCheckbox("Record video", "video")
		print "<fieldset><legend>Project parameters</legend><p>"
		f.display()
		print "</fieldset>"
	
class Pav(Project):
	def __init__(self, name, notes, video, \
			action_count, wait_time_min, wait_time_max):
		
		super(Pav,self).__init__(name, notes, video)
		self.action_count = action_count
		self.wait_time_min = wait_time_min
		self.wait_time_max = wait_time_max
		self.wait_times = []

	def __str__(self):
		return "[PAV] "+ super(Pav,self).__str__() + \
			"\nAction count: "+str(self.action_count) + \
			"\nWait time min: "+str(self.wait_time_min) +" sec" +\
			"\nWait time max: "+str(self.wait_time_max) +" sec" +\
			"\nWait time average (planned): "+str((self.wait_time_min+self.wait_time_max)/2) +" sec"
	
	def html(self):
		return super(Pav,self).html() +\
			"<p>" +\
			"<b>Type: </b> Pavlovian" +\
			"<br><b>Action count: </b>"+str(self.action_count) +\
			"<br><b>Minimum wait time: </b>" + str(self.wait_time_min) +" sec" +\
			"<br><b>Maximum wait time: </b>" + str(self.wait_time_max) +" sec" +\
			"<br><b>Average wait time (planned): </b>" + str((self.wait_time_min+self.wait_time_max)/2) +" sec"+\
			"</p>"			
	
	def passArgs(self, form):
		super(Pav,self).passArgs(form)

		form.addArgPass("pav", "ptype")
		form.addArgPass(self.action_count, "action_count")
		form.addArgPass(self.wait_time_min, "wait_time_min")
		form.addArgPass(self.wait_time_max, "wait_time_max")
	
	def run(self):
		super(Pav,self).run()
		
		import time
		from progressbar import progress
		from random import uniform as random_float

		#Reset since start stopwatch
		self.since_start.reset()
		
		#Log start
		self.log.append((0,0,"Start"))
		
		#Start doing the tasks
		current_task = 0
		for current_task in range(self.action_count):
			
			#Update progressbar
			progress(current_task*100/self.action_count)
			
			#Execute stimulus command
			self.stimulus()
			
			#Reset since stim stopwatch
			self.since_stim.reset()
			
			#Log the stimulus
			self.log.append((self.since_start.value(), 0, "Stimulus"))
			print "Tone at	"+ str(self.since_start)

			#Wait until the stim is over. Detect premature licks.
			self.stim_timer.reset()
			while self.stim_timer.is_running():
				if self.sensor.detected():
					self.log.append((self.since_start.value(), self.since_stim.value(), "Lick (premature)"))
					print "Lick at	" + str(self.since_start) +"	Since stim.	" +str(self.since_stim)+ " //Premature"
					
				time.sleep(0.001)
				
			#Give water
			self.water_valve.pulse()	
			
			#Log the water
			self.log.append((self.since_start.value(), self.since_stim.value(), "Water"))
			print "Water at	" + str(self.since_start) +"	Since stim.	" +str(self.since_stim)
			
			#Generate random wait time
			wait_time = random_float(self.wait_time_min,self.wait_time_max)
			
			#Log wait time
			self.wait_times.append(wait_time)
			print "Wait time	"+mtools.toString(wait_time)+" sec"
			
			#Set new time and reset the main timer
			self.main_timer.set(wait_time)
			self.main_timer.reset()
			
			#Wait until next stim. Log licks
			while self.main_timer.is_running():
				if self.sensor.detected():
					self.log.append((self.since_start.value(), self.since_stim.value(), "Lick"))
					print "Lick at	" + str(self.since_start) +"	Since stim.	" +str(self.since_stim)
				time.sleep(0.001)
		
		#Log end of project
		self.log.append((self.since_start.value(), self.since_stim.value(), "End"))
		
		#Calculate wait time statistics
		average_wait_time = mtools.avg(self.wait_times)
		wait_time_deviation = mtools.dev(self.wait_times)
		
		#Create specific logs
		licks_log = filter(lambda record: record[2]=="Lick" or record[2]=="Lick (premature)", self.log)
		reaction_times = map(lambda record: record[1], licks_log)
		
		#Calculate lick statistics
		average_reaction_time = mtools.avg(reaction_times)
		reaction_time_deviation = mtools.dev(reaction_times)
		
		#Create log files
		main_logfile = open("running/log.txt", "w")
		licks_logfile = open("running/licks.csv", "w")
		
		#Write logfile headers
		main_logfile.write(str(self)+"\n")
		main_logfile.write("Average wait time: " + mtools.toString(average_wait_time, padded=False) +" sec\n")
		main_logfile.write("Wait time deviation: " + mtools.toString(wait_time_deviation, padded=False) +" sec\n")
		main_logfile.write("Average reaction time: " + mtools.toString(average_reaction_time, padded=False) +" sec\n")
		main_logfile.write("Reaction time deviation: " + mtools.toString(reaction_time_deviation, padded=False) +" sec\n\n")
				
		licks_logfile.write("time[s],since_last_stim[s]\n")
		
		#Write records into log files
		for record in self.log:
			main_logfile.write(mtools.toString(record[0])+"	"+mtools.toString(record[1])+"	"+record[2]+"\n")
		
		for record in licks_log:
			licks_logfile.write(str(record[0])+","+str(record[1])+"\n")
		
		main_logfile.close()
		licks_logfile.close()
		
	@staticmethod
	def showForm(stim_type="audio", action_count=100, wait_time_min=45.0, wait_time_max=60.0, parent=None):
		
		f = mcgi.Form("step_3.py")
		stim_select = mcgi.Form.Select("Stimulus type", "stim_type")
		stim_select.addOption("Olfactory", "olfactory", selected=[False, True][stim_type=="olfactory"])
		stim_select.addOption("Audio", "audio", selected=[False, True][stim_type=="audio"])
		stim_select.addOption("Visual", "visual", selected=[False, True][stim_type=="visual"])
		f.addSelect(stim_select)
		
		if action_count is None:
			f.addInput("#of iterations", "action_count", warning="Please set this to a number (integer)")
		else:
			f.addInput("#of iterations", "action_count", value=action_count)
		
		if wait_time_min is None:
			f.addInput("Minimum wait time between stimuli", "wait_time_min",  warning="Please set this to a time in seconds", unit="sec")			
		else:
			f.addInput("Minimum wait time between stimuli", "wait_time_min", value=wait_time_min, unit="sec")
		
		if wait_time_max is None:
			f.addInput("Maximum wait time between stimuli", "wait_time_max",  warning="Please set this to a time in seconds", unit="sec")			
		else:
			f.addInput("Maximum wait time between stimuli", "wait_time_max", value=wait_time_max, unit="sec")
			
		#Pass the properties we already know about from last step.
		if parent is not None: parent.passArgs(f)
		f.addArgPass("pav", "ptype")
		
		print "<fieldset><legend>Pavlovian parameters</legend><p>"
		f.display()
		print "</fieldset>"

class OlfactoryPav(Pav):
	def __init__(self, name, notes, video, \
			action_count, wait_time_min, wait_time_max, \
			odor_valve_name, stim_length):	

		super(OlfactoryPav, self).__init__(name, notes, video, action_count, wait_time_min, wait_time_max)
		self.odor_valve_name = odor_valve_name
		self.stim_length = stim_length
		
		self.odor_valve = mvalve.Valve(pin = mconfig.odor_pin[odor_valve_name], pulse_length = mconfig.stim_length)
	
	def __str__(self):
		return "[OlfactoryPav] " + super(OlfactoryPav,self).__str__() + \
			"\nOdor valve: " + self.odor_valve_name + \
			"\nStim length: " + str(self.stim_length) +" sec"
	
	def html(self):	
		return super(OlfactoryPav,self).html() +\
			"<p>" +\
			"<b>Stimulus type: </b> Olfactory" +\
			"<br><b>Odor valve: </b>" + self.odor_valve_name +\
			"<br><b>Stim length: </b>" + str(self.stim_length) +" sec"	
	
	def passArgs(self, form):
		super(OlfactoryPav,self).passArgs(form)
		
		form.addArgPass("olfactory", "stim_type")
		form.addArgPass(self.odor_valve_name, "odor_valve_name")

		form.addArgPass(self.stim_length, "stim_length")	
	
	def run(self):

		self.stimulus = getattr(self.odor_valve, 'pulse')	#self.stimulus() will execute self.odor_valve.pulse()	
		
		#Run Pavlovian conditioning with the odor valve pulse as the stimulus
		super(OlfactoryPav,self).run()

		
	@staticmethod
	def showForm(odor_valve_name="A", stim_length=1.5, parent=None):
		f = mcgi.Form("step_4.py")
		
		r = mcgi.Form.Radio(title="Odor valve", name="odor_valve_name")
		r.addOption(title="A", value="A", checked=[False, True][positive_valve=="A"])
		r.addOption(title="B", value="B", checked=[False, True][positive_valve=="B"])
		r.addOption(title="C", value="C", checked=[False, True][positive_valve=="C"])
		r.addOption(title="D", value="D", checked=[False, True][positive_valve=="D"])
		r.addOption(title="E", value="E", checked=[False, True][positive_valve=="E"])

		f.addRadio(r)
		
		if stim_length is None:
			f.addInput("Length", "stim_length", warning="Please set this to a time in seconds", unit="sec")	
		else:
			f.addInput("Length", "stim_length", value=str(stim_length), unit="sec")	
		
		print "<fieldset><legend>Olfactory parameters</legend><p>"
		
		#Pass the properties we already know about from last step.	
		if parent is not None: parent.passArgs(f)
		f.addArgPass("olfactory", "stim_type")
		
		f.display()
		print "</fieldset>"		
		
class AudioPav(Pav):
	def __init__(self, name, notes, video, \
			action_count, wait_time_min, wait_time_max, \
			tone_hz, tone_type, stim_length):
			
		super(AudioPav, self).__init__(name, notes, video, action_count, wait_time_min, wait_time_max)
		self.tone_hz = tone_hz
		self.tone_type = tone_type
		self.stim_length = stim_length
		
		if self.tone_type in waves:
			self.tone_text = str(self.tone_hz) +" Hz " + str(self.tone_type) +" wave"
		elif self.tone_type == "pluck":
			self.tone_text = str(self.tone_hz) +" Hz " + str(self.tone_type)
		else:
			self.tone_text = str(self.tone_type)

	
	def __str__(self):
		return "[AudioPav] " + super(AudioPav,self).__str__() + \
			"\nPositive tone: " + self.tone_text + \
			"\nStim length: " + str(self.stim_length) +" sec"
			
	def html(self):	
		return super(AudioPav,self).html() +\
			"<p>" +\
			"<b>Stimulus type: </b> Audio" +\
			"<br><b>Tone: </b>" + self.tone_text +\
			"<br><b>Stim length: </b>" + str(self.stim_length) +" sec"
			
	def passArgs(self, form):
		super(AudioPav,self).passArgs(form)
		
		form.addArgPass("audio", "stim_type")
		form.addArgPass(self.tone_hz, "tone_hz")
		form.addArgPass(self.tone_type, "tone_type")
		
		form.addArgPass(self.stim_length, "stim_length")
	
	def run(self):
		#Import audio library and setup a tone as audio stim.
		import maudio
		maudio.init()
		tone = maudio.sound("pav_tone", self.tone_hz, self.tone_type, self.stim_length)
		self.stimulus = getattr(tone, 'play')	#self.stimulus() will execute tone.play()
		
		#Run Pavlovian conditioning with the tone as the stimulus
		super(AudioPav,self).run()
				
		#Stop audio module
		maudio.quit()
		
		
	@staticmethod
	def showForm(tone_hz=440, tone_type="sine", stim_length=1.0, parent=None):
		f = mcgi.Form("step_4.py")
		
		#Tone
		tone_select = mcgi.Form.Select("", "tone_type")
		tone_select.addOption("Sine wave", "sine", selected=[False, True][tone_type=="sine"])
		tone_select.addOption("Square wave", "square", selected=[False, True][tone_type=="square"])
		tone_select.addOption("Sawtooth wave", "sawtooth", selected=[False, True][tone_type=="sawtooth"])
		tone_select.addOption("Triangle wave", "triangle", selected=[False, True][tone_type=="triangle"])
		tone_select.addOption("Trapezium wave", "trapezium", selected=[False, True][tone_type=="trapezium"])

		tone_select.addOption("Pluck", "pluck", selected=[False, True][tone_type=="pluck"])

		tone_select.addOption("White noise", "whitenoise", selected=[False, True][tone_type=="whitenoise"])
		tone_select.addOption("Pink noise", "pinknoise", selected=[False, True][tone_type=="pinknoise"])
		tone_select.addOption("Brown noise", "brownnoise", selected=[False, True][tone_type=="brownnoise"])
		tone_select.addOption("TPDF noise", "tpdfnoise", selected=[False, True][tone_type=="tpdfnoise"])
		
		if tone_hz is None:
			f.addInput("Tone", "tone_hz", warning="Please set this to a frequency", unit="Hz", close_paragraph=False)	
		else:
			f.addInput("Tone", "tone_hz", value=str(tone_hz), unit="Hz", close_paragraph=False)	
			
		f.addSelect(tone_select)	
		
		#Stim. length
		if stim_length is None:
			f.addInput("Length", "stim_length", warning="Please set this to a time in seconds", unit="sec")	
		else:
			f.addInput("Length", "stim_length", value=str(stim_length), unit="sec")	
		
		print "<fieldset><legend>Audio parameters</legend><p>"
		
		#Pass the properties we already know about from last step.	
		if parent is not None: parent.passArgs(f)
		f.addArgPass("audio", "stim_type")
		
		f.display()
		print "</fieldset>"	
			
			
class Gng(Project):
	
	def __init__(self, name, notes, video, \
			action_count, positive_count, grace_preiod, active_period, idle_period, extra_time, reset_on_random):
			
		super(Gng,self).__init__(name, notes, video)

		self.action_count = action_count
		self.positive_count = positive_count
		self.negative_count = int(self.action_count) - int(self.positive_count)
		
		self.grace_preiod = grace_preiod
		self.active_period = active_period
		self.idle_period = idle_period
		
		self.extra_time = extra_time
		self.reset_on_random = reset_on_random

		
	
	def __str__(self):
		return "[GNG] "+ super(Gng,self).__str__() + \
			"\nAction count: "+str(self.action_count) + \
			"\nPositive count: "+str(self.positive_count) + \
			"\nNegative count: "+str(self.negative_count) + \
			"\nGrace period: " + str(self.grace_preiod) +" sec" + \
			"\nActive period: " + str(self.active_period) +" sec" + \
			"\nIdle period: " + str(self.idle_period) +" sec" + \
			"\nExtra time for wrong action: " + str(self.extra_time) +" sec" + \
			"\nReset on random action: " + str(self.reset_on_random) 
			
	def html(self):
		return super(Gng,self).html() +\
			"<p>" +\
			"<b>Type: </b> Go/No-Go" +\
			"<br><b>Action count: </b>"+str(self.action_count) +\
			"<br><b>Positive count: </b>"+str(self.positive_count) +\
			"<br><b>Negative count: </b>"+str(self.negative_count) +\
			"<br><b>Grace period: </b>" + str(self.grace_preiod) +" sec" +\
			"<br><b>Active period: </b>" + str(self.active_period) +" sec" +\
			"<br><b>Idle period: </b>" + str(self.idle_period) +" sec" +\
			"<br><b>Extra time for wrong action: </b>" + str(self.extra_time) +" sec" +\
			"<br><b>Reset on random action: </b>" + str(self.reset_on_random) +\
			"</p>"
	
	def passArgs(self, form):
		super(Gng,self).passArgs(form)

		form.addArgPass("gng", "ptype")
		form.addArgPass(self.action_count, "action_count")
		form.addArgPass(self.positive_count, "positive_count")
		
		form.addArgPass(self.active_period, "active_period")
		form.addArgPass(self.grace_preiod, "grace_preiod")
		form.addArgPass(self.idle_period, "idle_period")
		
		form.addArgPass(self.extra_time, "extra_time")		
		form.addArgPass(self.reset_on_random, "reset_on_random")

	def run(self):
		super(Gng,self).run()
		
		import time
		from random import shuffle
		from progressbar import progress
		from mtools import Timer
		
		active_timer = Timer(self.stim_length+2)
		
		#Todo list
		tasks = []
		
		#Put tasks with positive stimulus onto the todo list
		for i in range(project.positive_count):
			tasks.append(True)
			
		#Put tasks with negative stimulus onto the todo list
		for i in range(project.negative_count):
			tasks.append(False)

		#Execute tastks at random order
		shuffle(tasks)
			
		#Reset since start stopwatch
		self.since_start.reset()
		
		#Log start
		self.log.append((0,0,"Start"))
		
		#Start doing the tasks
		current_task_count = 1
		for current_task in tasks:
			
			#Update progressbar
			progress(current_task_count*100/len(tasks))
			
			#Stimulus
			self.since_stim.reset()
			if task:
				print "Positive stimulus"
				log.append((self.since_start.value(), self.since_stim.value(),"Positive stimulus"))
				self.positive_stimulus()
			else: 
				print "Negative stimulus"
				log.append((self.since_start.value(), self.since_stim.value(),"Negative stimulus"))
				self.negative_stimulus()

			#Grace period
			time.sleep(project.grace_preiod)
			
			#Wait until the stim is over. Detect premature licks.
			self.stim_timer.reset()
			while self.stim_timer.is_running():
				if self.sensor.detected():
					self.log.append((self.since_start.value(), self.since_stim.value(), "Lick (premature)"))
					print "Lick at	" + str(self.since_start) +"	Since stim.	" +str(self.since_stim)+ " //Premature"
					
				time.sleep(0.001)
			
			#Idle period
			eof_idle = time.time()+self.default_time
			while time.time() < eof_idle:
				if (GPIO.input(mconfig.sensor_pin)==1) and sensor_active:
					sensor_active = False
					print "Lick in idle phase"
					log.append((time.time()-start_time,"Random action ("+str(project.random_extra_time)+" sec)"))
					time.sleep(project.random_extra_time)
				
				if (GPIO.input(mconfig.sensor_pin)==0) and not sensor_active:
					sensor_active = True
			

			
			#Active period
			done = False
			eof_active = time.time()+project.stim_length+4 #Wait 2 extra second	s after the stimulus is over.
			
			while time.time() < eof_active:	
				#if not done:
				if (GPIO.input(mconfig.sensor_pin)==1) and not done:
					done = True
					print "Lick "+str(time.time()-start_time)
					log.append((time.time()-start_time,"Lick"))
					
					if task:
						print "Giving water"
						log.append((time.time()-start_time, "Drink"))
						drink()
	
					if not task:
						print "Punishing with time delay"
						log.append((time.time()-start_time, "Punishment delay ("+str(project.extra_time)+" sec)"))
						time.sleep(project.extra_time)
						log.append((time.time()-start_time, "Punishment over"))



			current_task_count += 1
		
		
		log.append((time.time()-start_time,"End"))		
	
	@staticmethod
	def showForm(stim_type="olfactory", action_count=30, positive_count=15, \
			grace_preiod=0.2, active_period=2.5, idle_period=3.0, extra_time=2.0, reset_on_random="on", parent=None):

		f = mcgi.Form("step_3.py")
		
		stim_select = mcgi.Form.Select("Stimulus type", "stim_type")
		stim_select.addOption("Olfactory", "olfactory", selected=[False, True][stim_type=="olfactory"])
		stim_select.addOption("Audio", "audio", selected=[False, True][stim_type=="audio"])
		stim_select.addOption("Visual", "visual", selected=[False, True][stim_type=="visual"])
		
		f.addSelect(stim_select)
		
		#Both action_count and positive_count are right
		if (action_count is not None) and (positive_count is not None):
			
			#If it doesn't make sense delete both fields and display error message
			if int(positive_count) > int(action_count):
				f.addInput("#of iterations", "action_count")
				f.addInput("#of positive stimuli", "positive_count", hint="#of negative stimuli will be calculated")
				f.addLabel('<font color="red">'+"The number of positive stimuli can't be greater than the number of iterations."+'</font>')
			
			#If it does make sense continue with the values
			else:
				f.addInput("#of iterations", "action_count", value=action_count)
				f.addInput("#of positive stimuli", "positive_count", value=positive_count, \
					hint="#of negative stimuli will be calculated")
		
		#Only action_count is wrong
		elif (action_count is None) and (positive_count is not None):
			f.addInput("#of iterations", "action_count", \
				warning="Please set this to a number (integer)")
			f.addInput("#of positive stimuli", "positive_count", \
				value=positive_count, \
				hint="#of negative stimuli will be calculated")
		
		#Only positive_count is wrong
		elif (positive_count is None) and (action_count is not None):
			f.addInput("#of iterations", "action_count",\
				value=action_count)
			f.addInput("#of positive stimuli", "positive_count", \
				warning="Please set this to a number (integer)", \
				hint="#of negative stimuli will be calculated")
		
		#Both are wrong
		elif (action_count is None) and (positive_count is None):
			f.addInput("#of iterations", "action_count", \
				warning="Please set this to a number (integer)")
			f.addInput("#of positive stimuli", "positive_count", \
				warning="Please set this to a number (integer)", \
				hint="#of negative stimuli will be calculated")		

		#Display error message if grace_preiod is NaN		
		if grace_preiod is None:
			f.addInput("Grace period ", "grace_preiod", \
				warning="Please set this to a time in seconds", unit="sec", \
				hint="Time period after stimulus in which all actions are ignored.")	
		else:
			f.addInput("Grace period ", "grace_preiod", value=grace_preiod, unit="sec", \
				hint="Time period after stimulus in which all actions are ignored.")
		
		#Display error message if active_period is NaN
		if active_period is None:
			f.addInput("Active period ", "active_period", \
				hint="Decision time given after the stimulus starts.", \
				warning="Please set this to a time in seconds", \
				unit="sec")
		else:
			f.addInput("Active period ", "active_period", \
				hint="Decision time given after the stimulus starts.", \
				value=active_period, \
				unit="sec")	
								
		#Display error message if idle_period is NaN
		if idle_period is None:
			f.addInput("Idle period ", "idle_period", \
				hint="Default time between tasks, without the punishment time.", \
				warning="Please set this to a time in seconds", unit="sec")	
		else:
			f.addInput("Idle period ", "idle_period", \
				hint="Default time between tasks, without the punishment time.", \
				value=idle_period, unit="sec")	
		

		#Display error message if extra_time is NaN		
		if extra_time is None:
			f.addInput("Time delay for wrong action ", "extra_time", \
				hint="Time that gets added to the idle period on failed tasks.", \
				warning="Please set this to a time in seconds",  unit="sec")
		else:
			f.addInput("Time delay for wrong action ", "extra_time", \
				hint="Time that gets added to the idle period on failed tasks.", \
				value=extra_time,  unit="sec")
		
		if reset_on_random == "on":
			f.addCheckbox("Reset on random action", "reset_on_random", \
				hint="Idle period will start over, if there is an action outside the active period.", \
				checked=True)
		else:
			f.addCheckbox("Reset on random action", "reset_on_random", \
				hint="Idle period will start over, if there is an action outside the active period.")
		
		#Pass the properties we already know about from last step.
		if parent is not None: parent.passArgs(f)
		f.addArgPass("gng", "ptype")
		
		print "<fieldset><legend>Go/NoGo parameters</legend><p>"
		f.display()
		print "</fieldset>"
		
class OlfactoryGng(Gng):

	def __init__ (self, name, notes, video, \
			action_count, positive_count, active_period, grace_preiod, idle_period, extra_time, reset_on_random, \
			positive_valve, negative_valve, blank_valve, stim_length):
			
		super(OlfactoryGng, self).__init__(name, notes, video, \
			action_count, positive_count, active_period, grace_preiod, idle_period, extra_time, reset_on_random)
		self.positive_valve = positive_valve
		self.negative_valve = negative_valve
		self.blank_valve = blank_valve
		self.stim_length = stim_length
	
	def __str__(self):
		return "[Olfactory] " + super(OlfactoryGng,self).__str__() +\
			"\nPositive valve: " + self.positive_valve +\
			"\nNegative valve: " + self.negative_valve +\
			"\nBlank valve: " + self.blank_valve +\
			"\nStim length: " + str(self.stim_length) +" sec"
	
	def html(self):
		return super(OlfactoryGng,self).html() +\
			"<p>" +\
			"<b>Stimulus type: </b> Olfactory" +\
			"<br><b>Positive valve: </b>" + self.positive_valve +\
			"<br><b>Negative valve: </b>" + self.negative_valve +\
			"<br><b>Blank valve: </b>" + self.blank_valve +\
			"<br><b>Stim length: </b>" + str(self.stim_length) +" sec"+\
			"</p>"
			
	def passArgs(self, form):
		super(OlfactoryGng,self).passArgs(form)
		
		form.addArgPass("olfactory", "stim_type")
		form.addArgPass(self.positive_valve, "positive_valve")
		form.addArgPass(self.negative_valve, "negative_valve")
		form.addArgPass(self.blank_valve, "blank_valve")
		form.addArgPass(self.stim_length, "stim_length")
		
	@staticmethod
	def showForm(positive_valve="A", negative_valve="B", blank_valve="C", stim_length=1.5, parent=None):
		f = mcgi.Form("step_4.py")
		
		pr = mcgi.Form.Radio(title="Positive fragrance valve", name="positive_valve")
		pr.addOption(title="A", value="A", checked=[False, True][positive_valve=="A"])
		pr.addOption(title="B", value="B", checked=[False, True][positive_valve=="B"])
		pr.addOption(title="C", value="C", checked=[False, True][positive_valve=="C"])
		pr.addOption(title="D", value="D", checked=[False, True][positive_valve=="D"])
		pr.addOption(title="E", value="E", checked=[False, True][positive_valve=="E"])
		f.addRadio(pr)

		nr = mcgi.Form.Radio(title="Negative fragrance valve", name="negative_valve")
		nr.addOption(title="A", value="A", checked=[False, True][negative_valve=="A"])
		nr.addOption(title="B", value="B", checked=[False, True][negative_valve=="B"])
		nr.addOption(title="C", value="C", checked=[False, True][negative_valve=="C"])
		nr.addOption(title="D", value="D", checked=[False, True][negative_valve=="D"])
		nr.addOption(title="E", value="E", checked=[False, True][negative_valve=="E"])
		f.addRadio(nr)
		
		br = mcgi.Form.Radio(title="Blank valve", name="blank_valve")
		br.addOption(title="A", value="A", checked=[False, True][blank_valve=="A"])
		br.addOption(title="B", value="B", checked=[False, True][blank_valve=="B"])
		br.addOption(title="C", value="C", checked=[False, True][blank_valve=="C"])
		br.addOption(title="D", value="D", checked=[False, True][blank_valve=="D"])
		br.addOption(title="E", value="E", checked=[False, True][blank_valve=="E"])
		f.addRadio(br)
		
		if positive_valve == negative_valve:
			f.addLabel('<font color="red">'+\
			"The positive and negative valve cannot be the same.<br>"\
			+'</font>')
			
		if positive_valve == blank_valve or negative_valve == blank_valve :
			f.addLabel('<font color="red">'+\
			"The fragrance and the blank valve cannot be the same.<br>"\
			+'</font>')
		
		if stim_length is None:
			f.addInput("Length", "stim_length", warning="Please set this to a time in seconds", unit="sec")	
		else:
			f.addInput("Length", "stim_length", value=str(stim_length), unit="sec")	
		
		print "<fieldset><legend>Olfactory parameters</legend><p>"
		
		#Pass the properties we already know about from last step.	
		if parent is not None: parent.passArgs(f)
		f.addArgPass("olfactory", "stim_type")
		
		f.display()
		print "</fieldset>"
		
class AudioGng(Gng):

	def __init__(self, name, notes, video, \
			action_count, positive_count, active_period, grace_preiod, idle_period, extra_time, reset_on_random,\
			positive_tone_hz, positive_tone_type, negative_tone_hz, negative_tone_type, stim_length):
			
		super(AudioGng, self).__init__(name, notes, video, \
			action_count, positive_count, active_period, grace_preiod, idle_period, extra_time, reset_on_random)
			
		self.positive_tone_hz = positive_tone_hz
		self.positive_tone_type = positive_tone_type
		self.negative_tone_hz = negative_tone_hz
		self.negative_tone_type = negative_tone_type
		#self.volume = volume
		self.stim_length = stim_length
				
		if self.positive_tone_type in waves:
			self.pos_tone_text = str(self.positive_tone_hz) +" Hz " + str(self.positive_tone_type) +" wave"
		elif self.positive_tone_type == "pluck":
			self.pos_tone_text = str(self.positive_tone_hz) +" Hz " + str(self.positive_tone_type)
		else:
			self.pos_tone_text = str(self.positive_tone_type)

		if self.negative_tone_type in waves:
			self.neg_tone_text = str(self.negative_tone_hz) +" Hz " + str(self.negative_tone_type) +" wave"
		elif self.negative_tone_type == "pluck":
			self.neg_tone_text = str(self.negative_tone_hz) +" Hz " + str(self.negative_tone_type)
		else:
			self.neg_tone_text = str(self.negative_tone_type)
		

	def __str__(self):		
		return "[AudioGng] " + super(AudioGng,self).__str__() + \
			"\nPositive tone: " + self.pos_tone_text + \
			"\nNegative tone: " + self.neg_tone_text + \
			"\nStim length: " + str(self.stim_length) +" sec"
		
	def html(self):		
		return super(AudioGng,self).html() +\
			"<p>" +\
			"<b>Stimulus type: </b> Audio" +\
			"<br><b>Positive tone: </b>" + self.pos_tone_text +\
			"<br><b>Negative tone: </b>" + self.neg_tone_text +\
			"<br><b>Stim length: </b>" + str(self.stim_length) +" sec"
			
		#"<br><b>Volume: </b>" + str(self.volume) + "%" +\	
			
	def passArgs(self, form):
		super(AudioGng,self).passArgs(form)
		
		form.addArgPass("audio", "stim_type")
		form.addArgPass(self.positive_tone_hz, "positive_tone_hz")
		form.addArgPass(self.positive_tone_type, "positive_tone_type")
		
		form.addArgPass(self.negative_tone_hz, "negative_tone_hz")
		form.addArgPass(self.negative_tone_type, "negative_tone_type")
		
		#form.addArgPass(self.volume, "volume")
		
		form.addArgPass(self.stim_length, "stim_length")

	def run(self):
		
		#Import audio library and setup a tones
		import maudio
		maudio.init()
		positive_tone = maudio.sound("pos_tone", self.positive_tone_hz, self.positive_tone_type, self.stim_length)
		negative_tone = maudio.sound("neg_tone", self.negative_tone_hz, self.negative_tone_type, self.stim_length)
		
		self.positive_stimulus = getattr(positive_tone, 'play')
		self.negative_stimulus = getattr(negative_tone, 'play')
		
		#Run Go/No-Go conditioning with the tone as the stimulus
		super(AudioGng,self).run()
				
		#Stop audio module
		maudio.quit()
		
	@staticmethod
	def showForm(positive_tone_hz=440, positive_tone_type="sine", negative_tone_hz=880, negative_tone_type="sine", stim_length=1.5, parent=None):
		f = mcgi.Form("step_4.py")
		
		#Positive tone
		positive_tone_select = mcgi.Form.Select("", "positive_tone_type")
		positive_tone_select.addOption("Sine wave", "sine", selected=[False, True][positive_tone_type=="sine"])
		positive_tone_select.addOption("Square wave", "square", selected=[False, True][positive_tone_type=="square"])
		positive_tone_select.addOption("Sawtooth wave", "sawtooth", selected=[False, True][positive_tone_type=="sawtooth"])
		positive_tone_select.addOption("Triangle wave", "triangle", selected=[False, True][positive_tone_type=="triangle"])
		positive_tone_select.addOption("Trapezium wave", "trapezium", selected=[False, True][positive_tone_type=="trapezium"])

		positive_tone_select.addOption("Pluck", "pluck", selected=[False, True][positive_tone_type=="pluck"])

		positive_tone_select.addOption("White noise", "whitenoise", selected=[False, True][positive_tone_type=="whitenoise"])
		positive_tone_select.addOption("Pink noise", "pinknoise", selected=[False, True][positive_tone_type=="pinknoise"])
		positive_tone_select.addOption("Brown noise", "brownnoise", selected=[False, True][positive_tone_type=="brownnoise"])
		positive_tone_select.addOption("TPDF noise", "tpdfnoise", selected=[False, True][positive_tone_type=="tpdfnoise"])
		
		if positive_tone_hz is None:
			f.addInput("Positive tone", "positive_tone_hz", warning="Please set this to a frequency", unit="Hz", close_paragraph=False)	
		else:
			f.addInput("Positive tone", "positive_tone_hz", value=str(positive_tone_hz), unit="Hz", close_paragraph=False)	
			
		f.addSelect(positive_tone_select)	
		
		
		#Negative tone
		negative_tone_select = mcgi.Form.Select("", "negative_tone_type")
		negative_tone_select.addOption("Sine wave", "sine", selected=[False, True][negative_tone_type=="sine"])
		negative_tone_select.addOption("Square wave", "square", selected=[False, True][negative_tone_type=="square"])
		negative_tone_select.addOption("Sawtooth wave", "sawtooth", selected=[False, True][negative_tone_type=="sawtooth"])
		negative_tone_select.addOption("Triangle wave", "triangle", selected=[False, True][negative_tone_type=="triangle"])
		negative_tone_select.addOption("Trapezium wave", "trapezium", selected=[False, True][negative_tone_type=="trapezium"])

		negative_tone_select.addOption("Pluck", "pluck", selected=[False, True][negative_tone_type=="pluck"])

		negative_tone_select.addOption("White noise", "whitenoise", selected=[False, True][negative_tone_type=="whitenoise"])
		negative_tone_select.addOption("Pink noise", "pinknoise", selected=[False, True][negative_tone_type=="pinknoise"])
		negative_tone_select.addOption("Brown noise", "brownnoise", selected=[False, True][negative_tone_type=="brownnoise"])
		negative_tone_select.addOption("TPDF noise", "tpdfnoise", selected=[False, True][negative_tone_type=="tpdfnoise"])
		
		if negative_tone_hz is None:
			f.addInput("Negative tone", "negative_tone_hz", warning="Please set this to a frequency", unit="Hz", close_paragraph=False)	
		else:
			f.addInput("Negative tone", "negative_tone_hz", value=str(negative_tone_hz), unit="Hz", close_paragraph=False)	
			
		f.addSelect(negative_tone_select)	
		
		f.addLabel("<i>Frequency will not be taken to account for noise types.</i>")
		
		#Volume
		"""
		if volume is None:
			f.addInput("Volume", "volume", warning="Please set this to a percentage", unit="%")	
		else:
			f.addInput("Volume", "volume", value=str(volume), unit="%")	
		"""		
		
		#Stim. length
		if stim_length is None:
			f.addInput("Length", "stim_length", warning="Please set this to a time in seconds", unit="sec")	
		else:
			f.addInput("Length", "stim_length", value=str(stim_length), unit="sec")	
		
		print "<fieldset><legend>Audio parameters</legend><p>"
		
		#Pass the properties we already know about from last step.	
		if parent is not None: parent.passArgs(f)
		f.addArgPass("audio", "stim_type")
		
		f.display()
		print "</fieldset>"		
		
class VisualGng(Gng):
	form = "visualgng_form.html"
	def __init__ (self, name, notes, video, \
			action_count, positive_count, active_period, grace_preiod, idle_period, extra_time, reset_on_random, \
			positive_animation, stim_length):
	
		super(VisualGng, self).__init__(name, notes, video, \
			action_count, positive_count, active_period, grace_preiod, idle_period, extra_time, reset_on_random)
			
		self.positive_animation = positive_animation
		self.negative_animation = "horizontal" if positive_animation=="vertical" else "vertical"
		self.stim_length = stim_length
	
	def __str__(self):
		return "[VisualGng] " + super(VisualGng, self).__str__() + \
			"\nPositive animation: " + self.positive_animation + \
			"\nNegative animation: " + self.negative_animation + \
			"\nStim length: " + str(self.stim_length) +" sec"
	
	def html(self):
		return super(VisualGng, self).html() +\
			"<p>" +\
			"<b>Stimulus type: </b> Visual" +\
			"<br><b>Positive animation: </b>" + self.positive_animation + \
			"<br><b>Negative animation: </b>" + self.negative_animation + \
			"<br><b>Stim length: </b>" + str(self.stim_length) +" sec"
			
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
