import Adafruit_CharLCD as LCD
from time import sleep
import threading

# Initialize the LCD using the pins 
lcd = LCD.Adafruit_CharLCDPlate()

#Setup triangle as select symbol
lcd.create_char(1, [6,4,4,12,12,4,4,6]) #Progress bar Left ending
lcd.create_char(2, [12,4,4,6,6,4,4,12]) #Progress bar Right ending
lcd.create_char(3, [8,12,10,9,10,12,8,0]) #Select triangle

# Clear the LCD
lcd.set_color(1.0, 0.0, 0.0)
lcd.clear()

class ControlPanel(object):
	def __init__(self):
		self.top_line = ""
		self.bottom_line = ""
		
		self.mode = "text"
		self.text = []
		self.current_line = 0
		
		self.options = []
		self.command = None
		
		self.up_active = True
		self.down_active = True
		self.left_active = True
		self.right_active = True
		self.select_active = True
		
		self.shift = 0
	
	def set_text(self, text):
		self.text = text.split("\n")
		if len(self.text) < 2: self.text.append("")
		
	def display_text(self):
		self.mode = "text"
		self.top_line = self.text[0]
		self.bottom_line = self.text[1]
		sleep(0.1)
		self.refresh()
		
	def display_progress(self, progress_percentage):
		if progress_percentage > 100: progress_percentage = 100 
		squares = chr(255)*(progress_percentage//10)
		self.bottom_line = "\x01" + squares.ljust(10) + "\x02" + str(progress_percentage) + '%'
		
		self.refresh()
	
	def animation(self, title):
		self.mode = "animation"
		self.top_line = title
		self.refresh()
		anim_thread = threading.Thread(target=self.animation_loop)
		anim_thread.start()
		
	def animation_loop(self):
		left = 0
		right = 11
		forward = True
		
		while self.mode == "animation": 
			self.bottom_line = "\x01" + " "*left+chr(255)*3+" "*right + "\x02" 
			self.refresh()
			if forward:
				left += 1
				right -= 1
			else:
				left -= 1
				right += 1
				
			if left == 11: forward = False
			if right == 11: forward = True
				
	def menu(self, title=None):
		selected = 5
		self.mode = "menu"
		if title is not None: 
			self.options.insert(0,title)
			selected = 1
		else:
			selected = 0
		
		self.top_line = [" ", "\x03"][selected==0]+self.options[0]
		self.bottom_line = [" ", "\x03"][selected==1]+self.options[1]
		
		print self.top_line
		print self.bottom_line
		
		
		self.refresh()
			
	def refresh(self):
		self.home()
		
		lcd.set_cursor(0,0)
		lcd.message(self.top_line.ljust(40))
		
		lcd.set_cursor(0,1)
		lcd.message(self.bottom_line.ljust(40))
	
	def start_checking(self):
		self.checking = True
		checkthread = threading.Thread(target=self.input_check_loop)
		checkthread.start()
		
	def stop_checking(self):
		self.checking = False
	
	def input_check_loop(self):
		while self.checking:
			self.check_inputs()
			sleep(0.1)
	
	def home(self):
		self.shift = 0
		lcd.home()
	
	def up_buttonpress(self):
		print "LCD up"
		if self.mode == "text":
			if self.current_line > 0:
				self.current_line -= 1
				self.top_line = self.text[self.current_line]
				self.bottom_line = self.text[self.current_line+1]
				self.refresh()
	
	def down_buttonpress(self):
		print "LCD down"
		if self.mode == "menu":
			if self.current_line < len(self.options)-2:
				self.current_line += 1
				self.top_line = self.text[self.current_line]
				self.bottom_line = self.text[self.current_line+1]
				self.refresh()
				
		if self.mode == "text":
			if self.current_line < len(self.text)-2:
				self.current_line += 1
				self.top_line = self.text[self.current_line]
				self.bottom_line = self.text[self.current_line+1]
				self.refresh()
		
	def left_buttonpress(self):
		print "LCD left"
		if self.mode == "text":
			if self.shift > 0: 
				lcd.move_right()
				self.shift -= 1	
		
	def right_buttonpress(self):
		print "LCD right"
		if self.mode == "text":
			if (len(self.top_line)-self.shift > 16) or (len(self.bottom_line)-self.shift > 16): 
				lcd.move_left()
				self.shift += 1	
		
	def select_buttonpress(self):
		print "LCD select"
		if self.mode == "text":
			self.menu()
	
	def check_inputs(self):
		#If UP is pressed
		if lcd.is_pressed(LCD.UP) and self.up_active:
			self.up_active = False
			self.up_buttonpress()
			
		#If DOWN is pressed
		if lcd.is_pressed(LCD.DOWN) and self.down_active:
			self.down_active = False
			self.down_buttonpress()
		
		#If LEFT is pressed
		if lcd.is_pressed(LCD.LEFT) and self.left_active:
			self.left_active = False
			self.left_buttonpress()		
			
		#If RIGHT is pressed
		if lcd.is_pressed(LCD.RIGHT) and self.right_active:
			self.right_active = False
			self.right_buttonpress()	
			
		#If SELECT is pressed
		if lcd.is_pressed(LCD.SELECT) and self.select_active:
			self.select_active = False
			self.select_buttonpress()
		
		#Reactivate unpressed buttons
		if not lcd.is_pressed(LCD.UP):
			self.up_active = True
		if not lcd.is_pressed(LCD.DOWN):
			self.down_active = True
		if not lcd.is_pressed(LCD.LEFT):
			self.left_active = True
		if not lcd.is_pressed(LCD.RIGHT):
			self.right_active = True
		if not lcd.is_pressed(LCD.SELECT):
			self.select_active = True
