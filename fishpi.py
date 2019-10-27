#!/usr/bin/python

#####################################################################################
# FISHPI																		HANS
# V1.2
#
# V0.0		21/02/15		herwerkt naar OOP stijl
# V1.0		22/02/15		Flask webserver toegevoegd
# V1.1		24/02/15		zonsondergang/opgang toegevoegd
# V1.2		25/02/15		Debug tijdklok()
#####################################################################################
# Sturing visbak
# Voor zonsopgang/ondergang wordt PyEphem gebruikt. pip install pyephem
#
#####################################################################################
#####IMPORT
###########
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
import RPi.GPIO as GPIO #GPIO importeren om te kunnen gebruiken
import time #sleep functie
from datetime import datetime, timedelta
from threading import Thread
import ephem

def tijdklok(tijd_aan, tijd_uit):
	now = datetime.now()
	now_mil = (now.hour)*100 + (now.minute)

	if tijd_aan == tijd_uit:
		return False
	elif (int(tijd_uit) > int(tijd_aan)) and (int(now_mil) >= int(tijd_aan)) and (int(now_mil) < int(tijd_uit)):
		return True
	elif (int(tijd_aan) > int(tijd_uit)) and ((int(now_mil) >= int(tijd_aan)) or (int(now_mil) < int(tijd_uit))):
		return True
	else:
		return False
		
def zonoffset(op_on, plus_min, offset_mil):
	o=ephem.Observer()  
	o.lat='51'  
	o.long='4'  
	s=ephem.Sun()  
	s.compute()
	
	if len(str(offset_mil)) > 2:
		offset_minuten = int(str(offset_mil)[(len(str(offset_mil))-2):len(str(offset_mil))]) + (int(str(offset_mil)[0:len(str(offset_mil))-2]))*60
	elif len(str(offset_mil)) == 2 or len(str(offset_mil)) == 1:
		offset_minuten = int(offset_mil)
	else:
		offset_minuten = 0
	if op_on == "op":
		if plus_min == "+":
			return (ephem.localtime(o.next_rising(s)) + timedelta(minutes=offset_minuten)).minute + \
					((ephem.localtime(o.next_rising(s)) + timedelta(minutes=offset_minuten)).hour)*100
		elif plus_min == "-":
			return (ephem.localtime(o.next_rising(s)) - timedelta(minutes=offset_minuten)).minute + \
					((ephem.localtime(o.next_rising(s)) - timedelta(minutes=offset_minuten)).hour)*100
		else:
			return 0
	elif op_on == "on":
		if plus_min == "+":
			return (ephem.localtime(o.next_setting(s)) + timedelta(minutes=offset_minuten)).minute + \
					((ephem.localtime(o.next_setting(s)) + timedelta(minutes=offset_minuten)).hour)*100
		elif plus_min == "-":
			return (ephem.localtime(o.next_setting(s)) - timedelta(minutes=offset_minuten)).minute + \
					((ephem.localtime(o.next_setting(s)) - timedelta(minutes=offset_minuten)).hour)*100
		else:
			return 0

	else:
		return 0		
		
		
def tijdconv(tijd):
	try:
		if str(tijd)[0:4] == "zop+":
			return zonoffset("op", "+", tijd[4:len(tijd)])
		elif str(tijd)[0:4] == "zop-":
			return zonoffset("op", "-", tijd[4:len(tijd)])
		elif str(tijd)[0:4] == "zon+":
			return zonoffset("on", "+", tijd[4:len(tijd)])
		elif str(tijd)[0:4] == "zon-":
			return zonoffset("on", "-", tijd[4:len(tijd)])
		else:
			return tijd
	except:
		print "fout in tijdentabel!"

class Uitgang(object):
	"""output object"""
	def __init__(self, pin):
		self.pin = pin
		self.naam = ""
		self.start_1 = "0"
		self.stop_1 = "0"
		self.start_2 = "0"
		self.stop_2 = "0"
		self.start_3 = "0"
		self.stop_3 = "0"
		self.start_4 = "0"
		self.stop_4 = "0"
		
		self.wstart_1 = "0" #w: werkelijke start, zop/zon ingecalculeerd
		self.wstop_1 = "0"
		self.wstart_2 = "0"
		self.wstop_2 = "0"
		self.wstart_3 = "0"
		self.wstop_3 = "0"
		self.wstart_4 = "0"
		self.wstop_4 = "0"
		
		self.auto = False
		self.hand_on = False
		
		self.output = False
		
	def toggle_hand_on(self):
		if int(self.hand_on) == 0:
			self.hand_on = 1
		else:
			self.hand_on = 0
			
	def toggle_modus(self):
		if int(self.auto) == 1:
			self.auto = 0
		else:
			self.auto = 1
							
	#~ def uitgang(self):
		#~ if int(self.auto) == 0:
			#~ return int(self.hand_on)
		#~ else:
			#~ return tijdklok(self.wstart_1,self.wstop_1) or \
				#~ tijdklok(self.wstart_2,self.wstop_2) or \
				#~ tijdklok(self.wstart_3,self.wstop_3) or \
				#~ tijdklok(self.wstart_4,self.wstop_4)
	
	def stuur_uitgang(self):
		self.wstart_1 = tijdconv(self.start_1)
		self.wstop_1 = tijdconv(self.stop_1)
		self.wstart_2 = tijdconv(self.start_2)
		self.wstop_2 = tijdconv(self.stop_2)
		self.wstart_3 = tijdconv(self.start_3)
		self.wstop_3 = tijdconv(self.stop_3)
		self.wstart_4 = tijdconv(self.start_4)
		self.wstop_4 = tijdconv(self.stop_4)
		
		GPIO.setup(self.pin, GPIO.OUT)
		if int(self.auto) == 0:
			GPIO.output(self.pin, int(self.hand_on))
		else:
			GPIO.output(self.pin, (tijdklok(self.wstart_1,self.wstop_1) or \
				tijdklok(self.wstart_2,self.wstop_2) or \
				tijdklok(self.wstart_3,self.wstop_3) or \
				tijdklok(self.wstart_4,self.wstop_4)))

def leesdata(Q):
	with open("/Visbak/tijden.csv", "r") as datafile:
		filedata = []
		lines = datafile.readlines()
		for lijn in lines:				
			filedata.append(lijn.split(";"))
		for pin in range (26):
			Q[pin].naam = ((str(filedata[pin][0])).strip())
			Q[pin].start_1 = ((str(filedata[pin][1])).strip())
			Q[pin].stop_1 = ((str(filedata[pin][2])).strip())
			Q[pin].start_2 = ((str(filedata[pin][3])).strip())
			Q[pin].stop_2 = ((str(filedata[pin][4])).strip())
			Q[pin].start_3 = ((str(filedata[pin][5])).strip())
			Q[pin].stop_3 = ((str(filedata[pin][6])).strip())
			Q[pin].start_4 = ((str(filedata[pin][7])).strip())
			Q[pin].stop_4 = ((str(filedata[pin][8])).strip())
			Q[pin].auto = ((str(filedata[pin][9])).strip())
			Q[pin].hand_on = ((str(filedata[pin][10])).strip())	
	print "Dataread tijden.csv " + str(datetime.now())

def savedata(Q):
	
	with open("/Visbak/tijden.csv", "r+") as datafile:
		lijnen = datafile.readlines()
		for lijn in range (26):
			lijnen[lijn] = ""
			lijnen[lijn] = (str(Q[lijn].naam) + ";" + \
							str(Q[lijn].start_1) + ";" + \
							str(Q[lijn].stop_1) + ";" + \
							str(Q[lijn].start_2) + ";" + \
							str(Q[lijn].stop_2) + ";" + \
							str(Q[lijn].start_3) + ";" + \
							str(Q[lijn].stop_3) + ";" + \
							str(Q[lijn].start_4) + ";" + \
							str(Q[lijn].stop_4) + ";" + \
							str(Q[lijn].auto) + ";" + \
							str(Q[lijn].hand_on) + "\n")
		
		datafile.seek(0) #Naar begin van file gaan
		for lijn in lijnen: 				
			datafile.write(str(lijn))#alle lijnen & voor & in file zetten.
		print "save tijden.csv: " + str(datetime.now())

def stuur_uitgangen(gebruikt, Q):
	try:
		while True:
			for pin in gebruikt:
				Q[pin].stuur_uitgang()
			time.sleep(0.5)
	except KeyboardInterrupt:
		GPIO.cleanup()		
def Main():
	GPIO.setmode(GPIO.BCM) #Nummering van de poorten gebruiken zoals op printplaat
	try:
		Q = [] #init
		alles = [4,17,21,22,10,9,11,7,24,25,8,7] 	#uitgangen zichtbaar op Bediening.html
		gebruikt = [4,17,21,22,10,9,11]				#uitgangen zichtbaar op Timetable.html
		
		for pin in range (26):						#voor iedere pin een Uitgangobject aanmaken
			Q.append(Uitgang(pin))
		
		thread1 = Thread(target = stuur_uitgangen, args=(gebruikt,Q,))
		thread1.daemon=True #Bij Ctrl-C ook de thread stoppen 
		
		leesdata(Q)
		thread1.start() #stuur_uitgangen in een thread starten zodat webserver parallel kan lopen
				
		print "Starting Flaskserver"
		app = Flask(__name__)
		
		@app.route('/bediening')
		def bediening():
			tijden = [] #initialiseren
			status = []
			modus = []
			naam = []
			for pin in range (26):
				status.append(str(Q[pin].hand_on))
				modus.append(str(Q[pin].auto))
				naam.append(str(Q[pin].naam))	
			templateData = {'naam' : naam,'status' : status,'modus' : modus,'gebruikt':alles}	
			return render_template("bediening.html", **templateData)
		
		@app.route('/modus/<pin>')
		def toggle_auto(pin):
			Q[int(pin)].toggle_modus()
			savedata(Q)
			return redirect('/bediening')
			
		@app.route('/hand/<pin>')
		def toggle_hand(pin):
			Q[int(pin)].toggle_hand_on()
			savedata(Q)
			return redirect('/bediening')
		
		@app.route('/timetable')
		def timetable():
			start_1 = []
			start_2 = []
			start_3 = []
			start_4 = []
			stop_1 = []
			stop_2 = []
			stop_3 = []
			stop_4 = []
		
			naam = []
		
			for pin in range (26):
				naam.append(str(Q[pin].naam))
				start_1.append(str(Q[pin].start_1))
				stop_1.append(str(Q[pin].stop_1))
				start_2.append(str(Q[pin].start_2))
				stop_2.append(str(Q[pin].stop_2))
				start_3.append(str(Q[pin].start_3))
				stop_3.append(str(Q[pin].stop_3))
				start_4.append(str(Q[pin].start_4))
				stop_4.append(str(Q[pin].stop_4))	
			templateData = {'naam' : naam,'gebruikt':gebruikt, 'start_1':start_1, 'stop_1':stop_1, \
							'start_2':start_2, 'stop_2':stop_2,  \
							'start_3':start_3, 'stop_3':stop_3,  \
							'start_4':start_4, 'stop_4':stop_4,	 \
							'zop': zonoffset("op","+","0000"), 'zon': zonoffset("on","+","0000")}
			return render_template("timetable.html", **templateData)
		
		@app.route('/submit', methods=['GET', 'POST'])
		def submit():
			rij = int(request.form['Q'])
			Q[rij].start_1 = str(request.form['start_1'])
			Q[rij].stop_1 = str(request.form['stop_1'])
			Q[rij].start_2 = str(request.form['start_2'])
			Q[rij].stop_2 = str(request.form['stop_2'])
			Q[rij].start_3 = str(request.form['start_3'])
			Q[rij].stop_3 = str(request.form['stop_3'])
			Q[rij].start_4 = str(request.form['start_4'])
			Q[rij].stop_4 = str(request.form['stop_4'])
			savedata(Q)
			return redirect('/timetable')
		
		@app.route('/home')
		def home():
			return render_template("home.html")
		
		@app.route('/')
		def root():
			return render_template("home.html")
	
		if __name__ == '__main__':
			#app.run(host='0.0.0.0', port=80, debug = True)
			app.run(host='0.0.0.0', port=80)
			
	except KeyboardInterrupt:
		GPIO.cleanup()

	finally:
		GPIO.cleanup()

if __name__ == '__main__':
	Main()

