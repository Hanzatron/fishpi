#!/usr/bin/python

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
import time
from threading import Thread
from multiprocessing import Process

def testfunction(timedata):
	timedata = timedata + "blah"
	
def Main():

	teststring = "blah"
	print teststring
	
	print "Starting Flaskserver"
	app = Flask(__name__)
	
	@app.route('/')
	def root():
		templateData = {'teststring' : teststring}
		return render_template("home.html",**templateData)
		
	if __name__ == '__main__':
		app.run(host='0.0.0.0', port=80)	
			
if __name__ == '__main__':
	Main()
