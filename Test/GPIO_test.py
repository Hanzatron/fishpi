#!/usr/bin/python

import RPi.GPIO as GPIO

poort = 7


GPIO.setmode(GPIO.BCM) #Nummering van de poorten gebruiken zoals op printplaat
GPIO.setup(poort, GPIO.OUT)

GPIO.output(poort, True)
