#!/usr/bin/python

import RPi.GPIO as GPIO #GPIO importeren om te kunnen gebruiken
import os
import time
from datetime import datetime 
GPIO.setmode(GPIO.BCM) #Nummering van de poorten gebruiken zoals op printplaat
GPIO.setup(17, GPIO.OUT)# poort 17 definieren als Output
try:
	while True:
		
		tijd_aan = 1010
		tijd_uit = 1025
		
		now = datetime.now()
		now_mil = (now.hour)*100 + (now.minute) #bij het uur 1 bijtellen om heel dat tijdzonegedoe op te lossen	
		
		if tijd_uit > now_mil >= tijd_aan:
			GPIO.output(17, True)
		else:
			GPIO.output(17, False)
		
		print now
		print now_mil
		time.sleep(1)
		os.system('clear')

except KeyboardInterrupt: #Actie na Ctrl-C: Alle gestuurde uitgangen vrijgeven
	GPIO.cleanup()

	
