#!/usr/bin/python

#####################################################################################
# CSV file bewerken															HANS
#
#####################################################################################
# De waarde in gegeven rij en kolom wijzigen door inhoud van new_value
#
# Eerst de volledige file inlezen, de nodige data aanpassen en dan de volledige file terug overschrijven
#
#####################################################################################


tijden = [] #initialiseren

rij = 4
kolom = 9
new_value = 1

with open("tijden.csv", "r+") as datafile:
	lines = datafile.readlines() #volledige file inlezen
	for lijn in lines: #data uit datafile lijn per lijn uitlezen				
				###Datalijn opspliten op scheidingsteken kolom
				tijden.append(lijn.split(";")) #aan list wordt telkens een list toegevoegd met de opgesplitste data
	tijden[rij][kolom] = new_value #data aanpassen
	lines[rij] = "" #bestaande lijn wissen
	for kolom in tijden[rij]:#alle items uit de list terug achtereen zetten met scheidingsteken ; ertussen
		lines[rij] = str(lines[rij]) + str(kolom) + ";"
	lines[rij] = lines[rij][0:((len(lines[rij])-1))] + "\n"	#laatste ; wissen en nieuwe regel toevoegen

	#inhoud terug schrijven naar file
	datafile.seek(0) #terug naar begin van de file gaan
	for lijn in lines: 				
			datafile.write(str(lijn))
	datafile.close()
