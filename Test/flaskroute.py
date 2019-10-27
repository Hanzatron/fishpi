from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
import shutil
import RPi.GPIO as GPIO #GPIO importeren om te kunnen gebruiken
import os
import time
from datetime import datetime
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
		
	###FLASK WEBSERVER
		
		app = Flask(__name__)

		gebruikt = [4,17,21,22,10,9,11]
		alles = [4,17,21,22,10,9,11,7,24,25,8,7]

		@app.route('/bediening')
		def bediening():
			tijden = [] #initialiseren
			status = []
			modus = []
			naam = []
			with open("/ramdrive/tijden.csv", "r+") as datafile:
				lines = datafile.readlines()
				for lijn in lines:				
					tijden.append(lijn.split(";"))
				for Q in range (26):
					status.append(tijden[Q][10].strip('\n'))
					modus.append(str(tijden[Q][9]))
					naam.append(str(tijden[Q][0]))	
			templateData = {'naam' : naam,'status' : status,'modus' : modus,'gebruikt':alles}	
			return render_template("bediening.html", **templateData)

		@app.route('/<modus>/<pin>')
		def toggle(modus,pin):
			tijden = [] #initialiseren

			rij = int(pin)
			if modus == "toggle":
				kolom = 10
			if modus == "modus":
				kolom = 9
			new_value = 1
	
			with open("/ramdrive/tijden.csv", "r+") as datafile:
				lines = datafile.readlines()
				for lijn in lines:				
					tijden.append(lijn.split(";"))
				if int(tijden[rij][kolom]) == 0:
					tijden[rij][kolom] = "1" 
				else:
					tijden[rij][kolom] = "0"
				lines[rij] = "" 
				for kolom in tijden[rij]:
					lines[rij] = str(lines[rij]) + str(kolom) + ";"
				lines[rij] = lines[rij][0:((len(lines[rij])-1))]
				lines[rij] = lines[rij].strip('\n') +"\n"
		
		
				datafile.seek(0)
				for lijn in lines: 				
					datafile.write(str(lijn))
				datafile.close()
				#wijziging opslaan op SD-kaart:
				shutil.copy2("/ramdrive/tijden.csv", "/Visbak/tijden.csv")
				print "copy tijden.csv to SD"
			return redirect('/bediening')

		@app.route('/timetable')
		def timetable():
			tijden = [] #initialiseren
			start_1 = []
			start_2 = []
			start_3 = []
			start_4 = []
			stop_1 = []
			stop_2 = []
			stop_3 = []
			stop_4 = []

			naam = []

			with open("/ramdrive/tijden.csv", "r+") as datafile:
				lines = datafile.readlines()
				for lijn in lines:				
					tijden.append(lijn.split(";"))
				for Q in range (26):
					naam.append(str(tijden[Q][0]))
					start_1.append(str(tijden[Q][1]))
					stop_1.append(str(tijden[Q][2]))
					start_2.append(str(tijden[Q][3]))
					stop_2.append(str(tijden[Q][4]))
					start_3.append(str(tijden[Q][5]))
					stop_3.append(str(tijden[Q][6]))
					start_4.append(str(tijden[Q][7]))
					stop_4.append(str(tijden[Q][8]))	
			templateData = {'naam' : naam,'gebruikt':gebruikt, 'start_1':start_1, 'stop_1':stop_1, \
							'start_2':start_2, 'stop_2':stop_2,  \
							'start_3':start_3, 'stop_3':stop_3,  \
							'start_4':start_4, 'stop_4':stop_4}
			return render_template("timetable.html", **templateData)

		@app.route('/submit', methods=['GET', 'POST'])
		def submit():
			tijden = [] #initialiseren
			rij = int(request.form['Q'])
			with open("/ramdrive/tijden.csv", "r+") as datafile:
				lines = datafile.readlines()
				for lijn in lines:				
					tijden.append(lijn.split(";"))
				tijden[rij][1] = str(request.form['start_1'])
				tijden[rij][2] = str(request.form['stop_1'])
				tijden[rij][3] = str(request.form['start_2'])
				tijden[rij][4] = str(request.form['stop_2'])
				tijden[rij][5] = str(request.form['start_3'])
				tijden[rij][6] = str(request.form['stop_3'])
				tijden[rij][7] = str(request.form['start_4'])
				tijden[rij][8] = str(request.form['stop_4'])
				lines[rij] = ""
				for kolom in tijden[rij]:
					lines[rij] = str(lines[rij]) + str(kolom) + ";"
				lines[rij] = lines[rij][0:((len(lines[rij])-1))]
				lines[rij] = lines[rij].strip('\n') +"\n"
		
				datafile.seek(0)
				for lijn in lines: 				
					datafile.write(str(lijn))
				datafile.close()
				#wijziging opslaan op SD-kaart:
				shutil.copy2("/ramdrive/tijden.csv", "/Visbak/tijden.csv")
				print "copy tijden.csv to SD"
			return redirect('/timetable')

		@app.route('/home')
		def home():
			return render_template("home.html")

		@app.route('/')
		def root():
			return render_template("home.html")

		if __name__ == '__main__':
			app.run(host='0.0.0.0', port=80, debug=True)
			
except KeyboardInterrupt: #Actie na Ctrl-C: Alle gestuurde uitgangen vrijgeven
	GPIO.cleanup()
