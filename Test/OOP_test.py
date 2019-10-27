#!/usr/bin/python
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
import time
from threading import Thread

class Uitgang(object):
	"""output object"""
	def __init__(self, modus, man_act):
		self.modus = modus
		self.man_act = man_act
		
	def status(self):
		return self.modus
	
	def toggle_modus(self):
		if self.modus == "auto":
			self.modus = "manueel"
		else:
			self.modus = "auto"
			
def autotoggle(output):
	while True:
		output.toggle_modus()
		#print "autotoggle :" + str(output.status())
		time.sleep(1)
			
def Main():

	Q4 = Uitgang("auto",0)
	
	print Q4.modus
	
	thread1 = Thread(target = autotoggle, args=(Q4,))
	thread1.start()

	print "Starting Flaskserver"
	app = Flask(__name__)
	
	@app.route('/')
	def root():
		templateData = {'modus' : Q4.status()}
		return render_template("test.html", **templateData)
	@app.route('/toggle')
	def toggle():
		Q4.toggle_modus()
		templateData = {'modus' : Q4.status()}
		return render_template("test.html", **templateData)

	if __name__ == '__main__':
		#app.run(host='0.0.0.0', port=80, debug=True)
		app.run(host='0.0.0.0', port=80)	
			
if __name__ == '__main__':
	Main()



