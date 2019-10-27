#!/usr/bin/python

import ephem  
from datetime import datetime
import datetime


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
			return (ephem.localtime(o.next_rising(s)) + datetime.timedelta(minutes=offset_minuten)).minute + \
					((ephem.localtime(o.next_rising(s)) + datetime.timedelta(minutes=offset_minuten)).hour)*100
		elif plus_min == "-":
			return (ephem.localtime(o.next_rising(s)) - datetime.timedelta(minutes=offset_minuten)).minute + \
					((ephem.localtime(o.next_rising(s)) - datetime.timedelta(minutes=offset_minuten)).hour)*100
		else:
			return 0
	elif op_on == "on":
		if plus_min == "+":
			return (ephem.localtime(o.next_setting(s)) + datetime.timedelta(minutes=offset_minuten)).minute + \
					((ephem.localtime(o.next_setting(s)) + datetime.timedelta(minutes=offset_minuten)).hour)*100
		elif plus_min == "-":
			return (ephem.localtime(o.next_setting(s)) - datetime.timedelta(minutes=offset_minuten)).minute + \
					((ephem.localtime(o.next_setting(s)) - datetime.timedelta(minutes=offset_minuten)).hour)*100
		else:
			return 0

	else:
		return 0		

def tijdconv(tijd):
	try:
		if str(tijd)[0:4] == "zop+":
			return zonsopgang("op") + int(tijd[4:len(tijd)])
		elif str(tijd)[0:4] == "zop-":
			return zonsopgang("op") - int(tijd[4:len(tijd)])
		elif str(tijd)[0:4] == "zon+":
			return zonsopgang("on") + int(tijd[4:len(tijd)])
		elif str(tijd)[0:4] == "zon-":
			return zonsopgang("on") - int(tijd[4:len(tijd)])
		else:
			return tijd
	except:
		print "fout in tijdentabel!"
		


start_1 = "zop+0100"
print zonoffset("op","+","0")
print zonoffset("op","+","100")
print zonoffset("op","-","0100")
print zonoffset("on","+","0")
print zonoffset("on","+","100")
print zonoffset("on","+","1")
print zonoffset("on","-","1")


