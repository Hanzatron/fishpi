#!/usr/bin/python


import RPi.GPIO as GPIO #GPIO importeren om te kunnen gebruiken
import time #sleep functie

pin = 2

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)

try:
    while True:
        GPIO.output(pin, 0)
        # time.sleep(30)

except KeyboardInterrupt: #Actie na Ctrl-C: Alle gestuurde uitgangen vrijgeven
    GPIO.cleanup()


