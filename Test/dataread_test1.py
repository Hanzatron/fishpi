#!/usr/bin/python



datafile = open("tijden.csv", "r")
i = 0
while i <= 24:
	datalijn = datafile.readline()
	i += 1
datafile.close()


data = tijden[1][0]
print data
