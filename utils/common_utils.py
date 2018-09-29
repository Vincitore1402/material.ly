from flask import flash, redirect, url_for, session
from functools import wraps
import json

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
	myFile = open(filename, mode='r', encoding='Latin-1')
	data = json.load(myFile)
	return data

# Write object to json file
def writeDataToFile(data, filename):
	myFile = open(filename, mode='w', encoding='Latin-1')
	json.dump(data, myFile)
	myFile.close()