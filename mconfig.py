#PIN CONFIG

#Select input and output pins BCM
i_pins = (4, 21)	
o_pins = (27, 17, 22)
v_pins = (19, 16, 26, 20, 21)

#The pin that the water valve is connected to.
drink_pin = o_pins[0]

#Odor valve pins
odor_pin = {'A':v_pins[0], \
			'B':v_pins[1], \
			'C':v_pins[2], \
			'D':v_pins[3], \
			'E':v_pins[4]}

#The pin that the lick sensor is connected to.
sensor_pin = i_pins[0]

#The pin that the positive stimulus is connected to.
positive_pin = o_pins[2]

#The pin that the negative stimulus is connected to.
negative_pin = o_pins[0]


#TIMES CONFIG

#Time the water valve is kept open (in seconds)
drink_time = 0.03

#Punishment time for random actions (in seconds). Set to 0 if random actions are not to be punished
random_action_delay = 1

#Punishment for incorrect action
punishment_time = 3

#Lenght of the stimuli in seconds
stim_length = 3

def GPIO_init():
	import RPi.GPIO as GPIO
	GPIO.setmode(GPIO.BCM)
	for i in i_pins:
		GPIO.setup(i, GPIO.IN)
			
	for o in o_pins:
		GPIO.setup(o, GPIO.OUT)
		GPIO.output(o, GPIO.LOW)
	
	for v in v_pins:
		GPIO.setup(v, GPIO.OUT)
		GPIO.output(v, GPIO.LOW)

#MISCELLANEOUS
#What is considered a wave list
waves = ["sine", "square", "sawtooth", "triangle", "trapezium"]
