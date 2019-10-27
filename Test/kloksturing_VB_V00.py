#!/usr/bin/python

#####################################################################################
# KLOKSTURING VISBAK															HANS
# V0.0
#
# V0.0		28/12/14		created
#
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

#####SET GPIO
#############
GPIO.setmode(GPIO.BCM) #Nummering van de poorten gebruiken zoals op printplaat
GPIO.setup(4, GPIO.OUT)# poort 17 definieren als Output
GPIO.setup(17, GPIO.OUT)# poort 4 definieren als Output
GPIO.setup(22, GPIO.OUT)# poort 22 definieren als Output

#####FUNCTIONS
##############

def tijdklok(tijd_mil, tijd_aan, tijd_uit):
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

#####PROGRAMMA
##############
 
cyclusteller = 0 #teller die bijhoudt hoeveel cyclussen het programma heeft doorlopen.
tijden = [[0 for x in range(9)] for x in range(24)] #2D array voor tijden uit file initialiseren

try:
	while True:
	###UUR UITLEZEN				
		now = datetime.now()
		now_mil = (now.hour)*100 + (now.minute)
		#inputstr = raw_input("Welke tijd simuleren?  ")
		#now_mil = int(inputstr)
		
	###TIJDEN UIT FILE LEZEN
	
		if cyclusteller == 0: #Datafile enkel openen als cyclusteller op 0 is gezet
			datafile = open("tijden.csv", "r")
			print "dataread op " + str(now)
			i = 0
			while i <= 23:
				datalijn = datafile.readline() #datafile lijn per lijn uitlezen
				###Datalijn opspliten op scheidingsteken kolom
				z = 0		
				start = 0
				datablok = 0
				scheidingsteken = ";"
				for z in range(len(datalijn)):					#ieder character in string scannen op scheidingsteken
					if datalijn[z] == scheidingsteken:			#als charakter scheidingsteken is
						tijden[i][datablok] = datalijn[start:z]	#deel van de string opslaan in array
						datablok += 1
						start = z + 1
				tijden[i][datablok] = datalijn[start:]
				###einde datalijn splitsen	
				i += 1 #volgende datalijn
			datafile.close()
		###Cyclusteller optellen en resetten
		cyclusteller += 1 
		if cyclusteller > 60:
			cyclusteller = 0
			
	###TIJDKLOKKEN UITLEZEN	
		
		switch_4 = tijdklok(now_mil,(tijden[4][1]),(tijden[4][2])) or \
					tijdklok(now_mil,(tijden[4][3]),(tijden[4][4])) or \
					tijdklok(now_mil,(tijden[4][5]),(tijden[4][6])) or \
					tijdklok(now_mil,(tijden[4][7]),(tijden[4][8]))
					
		GPIO.output(4, switch_4)
		
		switch_17 = tijdklok(now_mil,(tijden[17][1]),(tijden[17][2])) or \
					tijdklok(now_mil,(tijden[17][3]),(tijden[17][4])) or \
					tijdklok(now_mil,(tijden[17][5]),(tijden[17][6])) or \
					tijdklok(now_mil,(tijden[17][7]),(tijden[17][8]))
					
		GPIO.output(17, switch_17)
		
		switch_22 = tijdklok(now_mil,(tijden[22][1]),(tijden[22][2])) or \
					tijdklok(now_mil,(tijden[22][3]),(tijden[22][4])) or \
					tijdklok(now_mil,(tijden[22][5]),(tijden[22][6])) or \
					tijdklok(now_mil,(tijden[22][7]),(tijden[22][8]))
					
		GPIO.output(22, switch_22)
		
		time.sleep(59)
		#os.system('clear')

except KeyboardInterrupt: #Actie na Ctrl-C: Alle gestuurde uitgangen vrijgeven
	GPIO.cleanup()
