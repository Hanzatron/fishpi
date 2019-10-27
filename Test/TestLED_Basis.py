import RPi.GPIO as GPIO #GPIO importeren om te kunnen gebruiken
import time #er gaan tijdfuncties gebruik worden

GPIO.setmode(GPIO.BCM) #Nummering van de poorten gebruiken zoals op printplaat
GPIO.setup(4, GPIO.OUT)# poort 17 definieren als Output

inputstr = ""

try:
	while True:
		GPIO.output(4, True)


except KeyboardInterrupt: #Actie na Ctrl-C: Alle gestuurde uitgangen vrijgeven
	GPIO.cleanup()


