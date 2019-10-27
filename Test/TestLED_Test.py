import RPi.GPIO as GPIO #GPIO importeren om te kunnen gebruiken
import os 
GPIO.setmode(GPIO.BCM) #Nummering van de poorten gebruiken zoals op printplaat
GPIO.setup(17, GPIO.OUT)# poort 17 definieren als Output
try:
	while True:
		inputstr = raw_input("Uitgang 17 aan of uit?  ")

		if inputstr == "aan" or inputstr == "1":
			GPIO.output(17, True)
		else:
			GPIO.output(17, False)
		os.system('clear')

except KeyboardInterrupt: #Actie na Ctrl-C: Alle gestuurde uitgangen vrijgeven
	GPIO.cleanup()

	
