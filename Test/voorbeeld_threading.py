#!/usr/bin/python

#####################################################################################
# 
#####################################################################################
#
#
#
#####################################################################################
#####IMPORT
###########
import time
from datetime import datetime
from threading import Thread

a = 1

def functie1():
	while True:
		global a
		print str(a)
		time.sleep(0.5)
def functie2():
	while True:
		global a
		a = a + 1
		time.sleep(3)

		

def Main():
	
	thread1 = Thread(target = functie1, args=())
	thread2 = Thread(target = functie2, args=())
	thread1.start()
	thread2.start()
	
if __name__ == '__main__':
	Main()

