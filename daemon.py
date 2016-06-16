#!/usr/bin/python
import Adafruit_CharLCD as LCD
import os, time
import pickle
import mclass
import controlpanel

cp = controlpanel.ControlPanel()
cp.start_checking()
project = None

def wait_for_project():
	while not os.path.isfile("run/project.mcp"):
		if not cp.mode == "animation": cp.animation("Waiting...")
		time.sleep(0.5)
		
	#Load the project from file
	file = open("run/project.mcp", "rb")
	global project
	project = pickle.load(file)
	file.close()
	
	
	
	cp.command = None
	
	cp.options = ["Start", "Details", "Cancel"]
	cp.menu(title=project.name)
	
	time.sleep(0.5)
	cp.refresh()
	
	wait_for_input()
	
def wait_for_input():
	
	while cp.command is None:
		time.sleep(1)
	print cp.command + " was selected"
	
	if cp.command == "Start":
		project.run()
		time.sleep(3)
		cp.command = None
		cp.options = ["Start", "Details", "Cancel"]
		cp.menu(title=project.name)
		wait_for_input()		
		
	
	if cp.command == "Details":
		cp.set_text(str(project))
		while cp.command is not None:
			time.sleep(0.5)
		cp.options = ["Start", "Details", "Cancel"]
		cp.menu(title=project.name)
		wait_for_input()
		
	if cp.command == "Cancel":
		os.remove("run/project.mcp")
		wait_for_project()

def refresh(selected):
	lcd.home()
	lcd.set_cursor(0,1)
	lcd.message('\x03'+options[selected]+'   ')

def cancel_project():
	os.remove("run/project.mcp")

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


	


if __name__ == "__main__": Main()
