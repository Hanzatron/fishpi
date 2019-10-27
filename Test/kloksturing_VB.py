#!/usr/bin/python

#####################################################################################
# KLOKSTURING VISBAK															HANS
# V0.1
#
# V0.0		28/12/14		created
# V0.1		08/01/15		werking hetzelfde, programmatie simpeler gemaakt
# V1.0		22/01/15		hand/autofunctie toegevoegd
# V1.1		02/02/15		datafile lezen uit ramdrive en backup op SD
#####################################################################################
# Tijdschema wordt periodiek uit file tijden.csv gehaald. Omdat niet iedere programma
# cyclus de data uit de file zou gelezen worden wordt de cyclusteller gebruikt.
#
#
#
#####################################################################################
#####IMPORT
###########
import RPi.GPIO as GPIO #GPIO importeren om te kunnen gebruiken
import os
import time
from datetime import datetime 
import shutil

#####SET GPIO
#############
GPIO.setmode(GPIO.BCM) #Nummering van de poorten gebruiken zoals op printplaat
GPIO.setup(4, GPIO.OUT)		# TL GROEP 1
GPIO.setup(17, GPIO.OUT)	# TL GROEP 2
GPIO.setup(21, GPIO.OUT)	# TL GROEP 3
GPIO.setup(22, GPIO.OUT)	# SPOTJES
GPIO.setup(10, GPIO.OUT)	# KLEURLEDS
GPIO.setup(9, GPIO.OUT)		# VOEDERAUTOMAAT
GPIO.setup(11, GPIO.OUT)	# LUCHTBELLEN
GPIO.setup(24, GPIO.OUT)	# REGENPOMP
GPIO.setup(25, GPIO.OUT)	# ALARM
GPIO.setup(8, GPIO.OUT)		# ALARM INACTIEF
GPIO.setup(7, GPIO.OUT)		# STROBO

GPIO.setup(14, GPIO.IN)		# NIVEAUSWITCH HH
GPIO.setup(15, GPIO.IN)		# NIVEAUSWITCH LL
GPIO.setup(18, GPIO.IN)		# START REGEN
GPIO.setup(23, GPIO.IN)		# BEVESTIG ALARM

#####FUNCTIONS
##############

def tijdklok(tijd_mil, tijd_aan, tijd_uit): #check of huidige tijd binnen opgegeven tijden valt
	if tijd_aan == tijd_uit:
		return False
	else:	
		if tijd_aan < tijd_uit:
			if int(tijd_uit) > int(tijd_mil) and int(tijd_mil) >= int(tijd_aan):
				return True
			else:
				return False
		else:
			if int(tijd_mil) >= int(tijd_aan) or int(tijd_mil) < int(tijd_uit):
				return True
			else:
				return False

def switchcheck(outputnr): #in automatische modus schakelen op tijdklokken, anders in hand-modus
	if tijden[outputnr][9] == "1": #output staat in automatische modus
		return tijdklok(now_mil,(tijden[outputnr][1]),(tijden[outputnr][2])) or \
						tijdklok(now_mil,(tijden[outputnr][3]),(tijden[outputnr][4])) or \
						tijdklok(now_mil,(tijden[outputnr][5]),(tijden[outputnr][6])) or \
						tijdklok(now_mil,(tijden[outputnr][7]),(tijden[outputnr][8]))					
	else: #output staat in hand-modus
		return int(tijden[outputnr][10])

#####PROGRAMMA
##############
shutil.copy2("/Visbak/tijden.csv", "/ramdrive/tijden.csv")
print "Copy tijden.csv to ramdrive"
cyclusteller = 0 #teller die bijhoudt hoeveel cyclussen het programma heeft doorlopen.
#tijden = [[0 for x in range(10)] for x in range(25)] #2D array voor tijden uit file initialiseren
tijden = []
try:
	while True:
	###UUR UITLEZEN				
		now = datetime.now()
		now_mil = (now.hour)*100 + (now.minute)
		
	###TIJDEN UIT FILE LEZEN
	
		if cyclusteller == 0: #Datafile enkel openen als cyclusteller op 0 is gezet
			datafile = open("/ramdrive/tijden.csv", "r")
			print "dataread op " + str(now)
			lines = datafile.readlines()
			tijden = [] #tijden geheugen eerst wissen en daarna uitgelezen tijden toevoegen
			for lijn in lines: #data uit datafile lijn per lijn uitlezen				
				###Datalijn opspliten op scheidingsteken kolom
				tijden.append(lijn.split(";")) #aan list wordt telkens een list toegevoegd met de opgesplitste data
				###einde datalijn splitsen	
			datafile.close()
		###Cyclusteller optellen en resetten
		cyclusteller += 1 
		#print cyclusteller
		if cyclusteller > 1: #Waarde verhogen als de datafile niet iedere cyclus moet uitgelezen worden.
			cyclusteller = 0
			
	###UITGANGEN STUREN	
	
		GPIO.output(4, switchcheck(4))
		GPIO.output(17, switchcheck(17))
		GPIO.output(21, switchcheck(21))
		GPIO.output(22, switchcheck(22))
		GPIO.output(10, switchcheck(10))
		GPIO.output(11, switchcheck(11))
		
		time.sleep(0.5) #om de minuut uitgangen schakelen
		#os.system('clear')

except KeyboardInterrupt: #Actie na Ctrl-C: Alle gestuurde uitgangen vrijgeven
	GPIO.cleanup()
