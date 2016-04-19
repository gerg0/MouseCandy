import RPi.GPIO as GPIO
import mconfig
from time import sleep
import threading

class Valve(object):
	def __init__(self, pin, inverted=False, pulse_length=1):
		self.pin = pin
		self.inverted = inverted
		self.pulse_length = pulse_length
		self.set_close()

	def set_open(self):
		if self.inverted:
			GPIO.output(self.pin,GPIO.LOW)
		else:
			GPIO.output(self.pin,GPIO.HIGH)
		
	def set_close(self):
		if self.inverted:
			GPIO.output(self.pin,GPIO.HIGH)
		else:
			GPIO.output(self.pin,GPIO.LOW)
	
	def pulse_actions(self):
		self.set_open()
		sleep(self.pulse_length)
		self.set_close()
			
	def pulse(self):
		pthread = threading.Thread(target=self.pulse_actions)
		pthread.start()
		

