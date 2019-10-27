#!/usr/bin/python

tijden = [[0 for x in range(9)] for x in range(24)] #2D array initialiseren
datalijn = "Q1;800;1900;2000;2100;2200;2230;2300;2330"

z = 0		
start = 0
datablok = 0
scheidingsteken = ";"
for z in range(len(datalijn)):					#ieder character in string scannen op scheidingsteken
	if datalijn[z] == scheidingsteken:			#als charakter scheidingsteken is
		tijden [1][datablok] = datalijn[start:z]	#deel van de string opslaan in array
		datablok += 1
		start = z + 1
tijden [1][datablok] = datalijn[start:]				#laatste deel van string opslaan als laatste data

print tijden[1][0]
print tijden[1][1]
print tijden[1][2]
print tijden[1][3]
print tijden[1][4]
print tijden[1][5]
print tijden[1][6]
print tijden[1][7]
print tijden[1][8]

