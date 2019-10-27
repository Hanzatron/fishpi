#!/usr/bin/python

import RPi.GPIO as GPIO #GPIO importeren om te kunnen gebruiken
import os
import time
from datetime import datetime 
GPIO.setmode(GPIO.BCM) #Nummering van de poorten gebruiken zoals op printplaat
GPIO.setup(17, GPIO.OUT)# poort 17 definieren als Output

def tijdklok(tijd_mil, tijd_aan, tijd_uit):
	
	print tijd_aan
	if tijd_aan < tijd_uit:
		if tijd_uit > tijd_mil >= tijd_aan:
			return True
		else:
			return False
	else:
		if tijd_mil >= tijd_aan or tijd_mil < tijd_uit:
			return True
		else:
			return False

 
try:
	while True:
					
		now = datetime.now()
		#now_mil = (now.hour)*100 + (now.minute)
		inputstr = raw_input("Welke tijd simuleren?  ")
		now_mil = int(inputstr)
		
		switch_17 = tijdklok(now_mil,620,630) #tijden mogen niet met 0 beginnen! waarom weet ik niet
		
		GPIO.output(17, switch_17)
		
		#print now
		print now_mil
		print switch_17
		time.sleep(3)
		os.system('clear')

except KeyboardInterrupt: #Actie na Ctrl-C: Alle gestuurde uitgangen vrijgeven
	GPIO.cleanup()

	
