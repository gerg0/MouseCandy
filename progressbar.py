#!/usr/bin/python
import Adafruit_CharLCD as LCD

# Initialize the LCD using the pins 
lcd = LCD.Adafruit_CharLCDPlate()

lcd.set_color(1.0, 0.0, 0.0)
lcd.clear()

lcd.create_char(1, [6,4,4,12,12,4,4,6]) #Progress bar Left ending
lcd.create_char(2, [12,4,4,6,6,4,4,12]) #Progress bar Right ending

def progress(p):
	squares = p//10
	lcd.set_cursor(0, 1)
	lcd.message('\x01')
	
	for x in range(0, squares):
		lcd.message(chr(255))
	while squares < 10:
		lcd.message(' ')
		squares = squares + 1
	lcd.message('\x02' + str(p) + '%')
