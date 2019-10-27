#!/usr/bin/python

tijden =[]
datafile = open("tijden.csv", "r")
lines = datafile.readlines()
for line in lines:
	
	tijden.append(line.split(";"))

print tijden[0][1]

datafile.close()

