from flask import flash, redirect, url_for, session
from functools import wraps
import json, csv

def getConfig():
	import config.config as importedConfig
	return importedConfig.config

config = getConfig()

# Check if user logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Unauthorized, Please login', 'danger')
			return 	redirect(url_for('auth.login'))
	return wrap

# Read object from json file
def loadDataFromFile(filename):
	myFile = open(config.PROJECT_DIRECTORY + filename, mode='r', encoding='Latin-1')
	data = json.load(myFile)
	return data

# Write object to json file
def writeDataToFile(data, filename):
	myFile = open(config.PROJECT_DIRECTORY + filename, mode='w', encoding='Latin-1')
	json.dump(data, myFile)
	myFile.close()

# To do
def write_csv(filename, data):
    # with open (filename, 'w' ) as f:
	#fiiednames = ['1','2','3']
  #     writer = csv.Dictwriter(f, fieldnames=fieldnames)
	# 	writer.writeheader()
	with open (filename, 'w') as f:
		fieldnames = ['id','1','2', '3','4','5','6','7','8','9','10','11','12','13','14']
		writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator = '\n')
		writer.writeheader()

		for i in range(0, len(data)):
			writer.writerow({'id':data[i]['id'],'1': data[i]['composition'][0]['average'], '2': data[i]['composition'][1]['average'], '3':data[i]['composition'][2]['average'], '4':data[i]['composition'][3]['average'], '5':data[i]['composition'][4]['average'], '6':data[i]['composition'][5]['average'], '7':data[i]['composition'][6]['average'],'8':data[i]['composition'][7]['average'], '9':data[i]['composition'][8]['average'], '10':data[i]['composition'][9]['average'], '11':data[i]['composition'][10]['average'], '12':data[i]['composition'][11]['average'], '13':data[i]['composition'][12]['average'], '14':data[i]['composition'][13]['average']})