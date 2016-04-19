#!/usr/bin/python
import Adafruit_CharLCD as LCD
import os, time
import pickle
import mclass
import controlpanel

cp = controlpanel.ControlPanel()
cp.start_checking()


def wait_for_project():
	while not os.path.isfile("run/project"):
		if not cp.mode == "animation": cp.animation("Waiting...")
		time.sleep(0.5)

def wait_for_input():
	while cp.mode == "menu" and cp.command is None:
		time.sleep(1)

def refresh(selected):
	lcd.home()
	lcd.set_cursor(0,1)
	lcd.message('\x03'+options[selected]+'   ')

def cancel_project():
	os.remove("run/project")

def wait_for_user():
	global options
	global selected
	global main_loop
	selected = 0
	refresh(selected)
	waiting = True
	while waiting:
		
		#If UP is pressed
		if lcd.is_pressed(LCD.UP) and up_active:
			up_active = False
			
			if selected > 0: selected -= 1	
			refresh(selected)
			
		#If DOWN is pressed
		if lcd.is_pressed(LCD.DOWN) and down_active:
			down_active = False
			
			if selected < len(options)-1: selected += 1		
			refresh(selected)
			
		#If SELECT is pressed
		if lcd.is_pressed(LCD.SELECT) and select_active:
			select_active = False
			
			if options[selected] == "Start": 
				waiting = False
				#main_loop = False
				#print project.name
				project.run()
			
			if options[selected] == "Cancel": 
				waiting = False
				cancel_project()
		
		
		#Reactivate unpressed buttons
		if not lcd.is_pressed(LCD.UP):
			up_active = True
		if not lcd.is_pressed(LCD.DOWN):
			down_active = True
		if not lcd.is_pressed(LCD.SELECT):
			select_active = True
			
		time.sleep(0.1)
		
def Main():

	wait_for_project()
	
	#Load the project from file
	file = open("run/project", "rb")
	project = pickle.load(file)
	file.close()
	
	cp.options = ["Start", "Details", "Cancel"]
	cp.menu(title=project.name)

	wait_for_input()


if __name__ == "__main__": Main()
