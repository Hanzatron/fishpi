from flask import Flask
from flask import request
from flask import render_template
from flask import redirect

teststring = ""
app = Flask(__name__)

@app.route('/')
def home():
	teststring = 'variabele data'
	templateData = {'textdata' : teststring}
		
	return render_template("home.html", **templateData)

@app.route('/4_on')
def switch4():
	tijden = [] #initialiseren

	rij = 4
	kolom = 10
	new_value = 1
	
	with open("tijden.csv", "r+") as datafile:
		lines = datafile.readlines() #volledige file inlezen
		for lijn in lines: #data uit datafile lijn per lijn uitlezen				
				###Datalijn opspliten op scheidingsteken kolom
			tijden.append(lijn.split(";")) #aan list wordt telkens een list toegevoegd met de opgesplitste data
		
		datafile.close()
		print tijden[rij][kolom]
	if int(tijden[rij][kolom]) == 1:
		return "1"
	else:
		return "0"
	
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True)
