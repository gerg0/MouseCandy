from os import system
from pygame import mixer


def init():
	mixer.init()
	
def quit():
	mixer.quit()
	
"""
class MSound():
	def __init__(self, filename, freq, sound_type, length):
		self.freq = freq
		self.sound_type = sound_type
		self.length = length
		self.filename = "running/"+filename+".wav"
		
		system("sox -n -b 16 "+self.filename+" synth "+str(self.length)+" "+self.sound_type+" "+str(self.freq))

		return mixer.Sound(self.filename)
"""



def sound (filename, freq, sound_type, length):
	filename = "running/"+filename+".wav"
	system("sox -n -b 16 "+filename+" synth "+str(length)+" "+sound_type+" "+str(freq))
	#mixer.init()
	return mixer.Sound(filename)
