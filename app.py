from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, make_response, send_file
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps


from flask import Blueprint
from operator import attrgetter
import MySQLdb
import MySQLdb.cursors
import math
import time

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm
import numpy as np
import io

import plot_compare_methods as manifoldLearning

import pygal
from io import StringIO
import base64
import csv

import sys
sys.path.append('./config')
# Import config
import config
sys.path.remove('./config')

app = Flask(__name__)
app.secret_key = 'secret123'

def getConn():
	conn = MySQLdb.connect(host=config.DB_HOST, user=config.DB_USER, passwd=config.DB_PASSWORD, db=config.DB_NAME,charset=config.DEFAULT_CHARSET,cursorclass=MySQLdb.cursors.DictCursor)
	return conn

# Data visualisation Tests

@app.route("/manif_show")
def manif_plot():
	# Get data for Learning and check it for 0 in columns
	# dataForLearn = getDataForLearning()

	# Delete 0-data with mask
	# mask = np.any(np.not_equal(res, 0.), axis=0)
	# arr = res[:,mask]
	# arr = np.unique(arr, axis=0)
	# arr = arr[:]

	# Learning and get 2-dimensional data for plotting on a graph
	# manif = manifoldLearning.startLearning(dataForLearn)

	# writeToFile(manif, 'manifData.txt')
	# manif = loadFromFile('manifData.txt')

	# np.savetxt('manifData.csv', manif, delimiter = ';')
	# manif = np.loadtxt('manifData.csv', dtype=float, delimiter=';')
	
	

	from pygal.style import DarkStyle
	xy_chart = pygal.XY(stroke=False, x_title='K1, %', y_title='K2, %')

	# pygal_manif = []
	# for key, value in manif.items():
	# 	res = []
	# 	for i in range(0, len(value['x'])):
	# 		res.append({'value': [value['x'][i],value['y'][i]], 'label': str(value['matInfo'][i])})
	# 	pygal_manif.append((key, res))
	# 	# xy_chart.add(key, res)

	# writeToFile(pygal_manif, 'manifPygal.txt')
	# Need to use full path to deploy
	# home/rloveshhenko/myflaskapp
	pygal_manif = loadFromFile('manifPygal.txt')
	for item in pygal_manif:
		if (item[0] == 'Spectral Embedding'):
			continue
		xy_chart.add(item[0], item[1])
		print (item[0] + " :" + str(len(item[1])))
	
	
	#xy_chart.title = 'Dependence of the yield stress on the concentration of a chemical element'
	xy_chart.title = ''
	# xy_chart.add('Spectral Embedding', res)
	# xy_chart.add('Carboneum (С)', result['data1'])
	# xy_chart.add('B', [{'value': [.1,.15], 'label': 'Some plain text here'}, (.12, .23), (.4, .3), (.6, .4), (.21, .21), (.5, .3), (.6, .8), (.7, .8)])
	#xy_chart.add('C', [(.05, .01), (.13, .02), (1.5, 1.7), (1.52, 1.6), (1.8, 1.63), (1.5, 1.82), (1.7, 1.23), (2.1, 2.23), (2.3, 1.98)])
	graph_data = xy_chart.render_data_uri()
	return render_template('pygal.html', graph_data = graph_data)


@app.route('/data')
def getDataForLearning():
	import numpy as np

	# Getting data from DB
	conn = getConn()
	cur = conn.cursor()

	# Select all field from table except of ID 
	# SQL_SELECT = "SELECT "
	# for i in range(1,118):
	# 	SQL_SELECT += "`" +str(i) + "`" + ","
	# SQL_SELECT += "`" +str(118) + "`"
	# SQL_SELECT += " FROM rloveshhenko$mydbtest.composed_data"
	
	SQL_SELECT = "SELECT * FROM rloveshhenko$mydbtest.composed_data"
	SQL_SELECT_INFO = "SELECT classification,marka FROM rloveshhenko$mydbtest.main_info WHERE id in (SELECT id FROM rloveshhenko$mydbtest.composed_data)"

	cur.execute(SQL_SELECT)
	composed_data = cur.fetchall()

	cur.execute(SQL_SELECT_INFO)
	info = cur.fetchall()

	arrayData = []
	ids = []
	for d in composed_data:
		arr = np.array(list(dict(d).values())[1:]).astype(float)
		arrayData.append(arr)
		ids.append(list(dict(d).values())[:1][0])
	
	matInfo = []

	for i in info:
		listInfo = list(dict(i).values())
		matInfo.append(str(listInfo[0]) + " " + str(listInfo[1]))
	npArr = np.array(arrayData)
	
	# np.savetxt('out.csv', npArr)
	
	# Saving array to 
	with open('numpyData.csv', 'wb') as f:
		np.savetxt(f, npArr, fmt='%.5f')
	
	print ('Gotten data: ')
	print ('numpyArr: ' + str(len(npArr)))
	print ('ids: ' + str(len(ids)))
	return {
		'numpyArr' : npArr,
		'matInfo': matInfo,
		'ids': ids
	}


def get_sigma_t_for_chart_C():
	conn = getConn()
	cur = conn.cursor()
	cur.execute('SELECT main_info_id, sigma_t from rloveshhenko$mydbtest.mechanical_properties where  main_info_id in (SELECT main_info_id from rloveshhenko$mydbtest.chemical_composition where main_info_id in (SELECT main_info_id FROM rloveshhenko$mydbtest.mechanical_properties WHERE main_info_id in (SELECT id from rloveshhenko$mydbtest.main_info where classification like "%Сталь%") and sigma_t != " " and sigma_t != " ") and atomic_Number = 6)and sigma_t != " " ;')
	sigma_t = cur.fetchall()
	app.logger.info('sigma_t length: ' + str(len(sigma_t)))
	conn.close()
	result = []
	ID = []
	for i in range(0, len(sigma_t)):
		if sigma_t[i]['main_info_id'] not in ID:
			if ('-' in sigma_t[i]['sigma_t']):
				minimum = sigma_t[i]['sigma_t'].split('-')[0].strip()
				maximum = sigma_t[i]['sigma_t'].split('-')[1].strip()
				average = (float(minimum) + float(maximum))/2
				result.append(average)
				ID.append(sigma_t[i]['main_info_id'])
			else:
				result.append(sigma_t[i]['sigma_t'])
				ID.append(sigma_t[i]['main_info_id'])
            	#result.append(sigma_t[i]['sigma_t'])
				#ID.append(sigma_t[i]['main_info_id'])
	app.logger.info('sigma_t NEW REFACTORING length: ' + str(len(result)))
	return result

def get_averages_for_chart_C():
	conn = getConn()
	cur = conn.cursor()
	cur.execute('SELECT average from rloveshhenko$mydbtest.chemical_composition where main_info_id in (SELECT main_info_id FROM rloveshhenko$mydbtest.mechanical_properties WHERE main_info_id in (SELECT id from rloveshhenko$mydbtest.main_info where classification like "%Сталь%") and sigma_t != " " and sigma_t != " ") and atomic_Number = 6;')
	averages = cur.fetchall()
	app.logger.info('averages length: ' + str(len(averages)))
	conn.close()
	result = []
	for i in range(0, len(averages)):
		result.append(averages[i]['average'])
	return result

def get_sigma_t_for_chart_Si():
	conn = getConn()
	cur = conn.cursor()
	cur.execute('SELECT main_info_id, sigma_t from rloveshhenko$mydbtest.mechanical_properties where  main_info_id in (SELECT main_info_id from rloveshhenko$mydbtest.chemical_composition where main_info_id in (SELECT main_info_id FROM rloveshhenko$mydbtest.mechanical_properties WHERE main_info_id in (SELECT id from rloveshhenko$mydbtest.main_info where classification like "%Сталь%") and sigma_t != " " and sigma_t != " ") and atomic_Number = 14)and sigma_t != " " ;')
	sigma_t = cur.fetchall()
	app.logger.info('sigma_t length: ' + str(len(sigma_t)))
	conn.close()
	result = []
	ID = []
	for i in range(0, len(sigma_t)):
		if sigma_t[i]['main_info_id'] not in ID:
			if ('-' in sigma_t[i]['sigma_t']):
				minimum = sigma_t[i]['sigma_t'].split('-')[0].strip()
				maximum = sigma_t[i]['sigma_t'].split('-')[1].strip()
				average = (float(minimum) + float(maximum))/2
				result.append(average)
				ID.append(sigma_t[i]['main_info_id'])
			else:
				result.append(sigma_t[i]['sigma_t'])
				ID.append(sigma_t[i]['main_info_id'])
            	#result.append(sigma_t[i]['sigma_t'])
				#ID.append(sigma_t[i]['main_info_id'])
	app.logger.info('sigma_t NEW REFACTORING length: ' + str(len(result)))
	return result

def get_averages_for_chart_Si():
	conn = getConn()
	cur = conn.cursor()
	cur.execute('SELECT average from rloveshhenko$mydbtest.chemical_composition where main_info_id in (SELECT main_info_id FROM rloveshhenko$mydbtest.mechanical_properties WHERE main_info_id in (SELECT id from rloveshhenko$mydbtest.main_info where classification like "%Сталь%") and sigma_t != " " and sigma_t != " ") and atomic_Number = 14;')
	averages = cur.fetchall()
	app.logger.info('averages length: ' + str(len(averages)))
	conn.close()
	result = []
	for i in range(0, len(averages)):
		result.append(averages[i]['average'])
	return result

def composeDataForChart():
	data = []
	data2 = []
	averages = get_averages_for_chart_C()
	sigmas = get_sigma_t_for_chart_C()

	for i in range (0, len(averages)):
		data.append((float(averages[i]), float(sigmas[i])))

	averages = get_averages_for_chart_Si()
	sigmas = get_sigma_t_for_chart_Si()
	for i in range (0, len(averages)):
		data2.append((float(averages[i]), float(sigmas[i])))

	result = {
		'data1' : data,
		'data2' : data2
	}
	writeToFile(result, 'chartData.txt')
	return result

# Write object to json file
def writeToFile(data, filename):
	import json
	myFile = open(filename, mode='w', encoding='Latin-1')
	json.dump(data, myFile)
	myFile.close()

# Read object from json file
def loadFromFile(filename):
	import json
	myFile = open(filename, mode='r', encoding='Latin-1')
	data = json.load(myFile)
	return data

# Function to sort tuple by atomic numbers
def getKeyForAtomicNumbers(item):
	return item['atomic_Number']

def getChemicalCompositionData():
	conn = getConn()
	cur = conn.cursor()
	cur.execute('SELECT main_info_id, atomic_Number, average FROM mydbtest.chemical_composition WHERE main_info_id in (SELECT id FROM mydbtest.main_info WHERE classification like "%Сталь%");')
	dataDb = cur.fetchall()

	cur.execute('SELECT distinct main_info_id FROM mydbtest.chemical_composition WHERE main_info_id in (SELECT id FROM mydbtest.main_info WHERE classification like "%Сталь%");')
	ids = cur.fetchall()

	cur.execute('SELECT atomic_Number, symbol FROM mydbtest.periodic_table ORDER BY atomic_Number;')
	atomicElements = cur.fetchall()

	atomicElementsRefactor = []

	for i in range(0, len(atomicElements)):
		atomicElementsRefactor.append(atomicElements[i]['atomic_Number'])

	# print ('Length: ' + str(len(ids)))
	# print (dataDb[0])
	conn.close()
	result = []
	for i in range(0,len(ids)):
		info = []
		for j in range (0, len(dataDb)):
			if (dataDb[j]['main_info_id'] == ids[i]['main_info_id']):
				# Add a 0 averages frpm others elements

				# for k in range(0, len(atomicElements)):
				# 	if (atomicElements[k]['atomic_Number'] in dataDb['atomic_Number']):
				# 		data = {
				# 			"atomic_Number" : dataDb[j]['atomic_Number'],
				# 			"average" : dataDb[j]['average']
				# 		}
				# 	else:
				# 		data = {
				# 			"atomic_Number" : dataDb[j]['atomic_Number'],
				# 			"average" : 0
				# 		}
				info.append({
					"atomic_Number" : dataDb[j]['atomic_Number'],
					"average" : dataDb[j]['average']
				})
		infoAtNumb = []
		for k in range(0, len(info)):
			infoAtNumb.append(info[k]['atomic_Number'])

		for k in range(0, len(atomicElementsRefactor)):
			if (atomicElementsRefactor[k] not in infoAtNumb):
				info.append({
					"atomic_Number" : atomicElementsRefactor[k],
					"average" : 0
				})
		sortedInfo = sorted(info, key=getKeyForAtomicNumbers)
		# avgSum = 0.0
		# for i in range(0,len(sortedInfo)):
		# 	try:
		# 		avgSum += float(sortedInfo[i]['average'])
		# 	except:
		# 		avgSum += 0
		#
		# sortedInfo[25]['average'] = 1 - avgSum
		avgSum = 0.0
		for elem in sortedInfo:
			try:
				avgSum += float(elem['average'])
			except:
				avgSum += 0
		print(avgSum)
		if (100 - avgSum > 0):
			sortedInfo[25] = {
				"atomic_Number" : 26,
				"average" : 100 - avgSum
			}
		result.append({
			"id" : ids[i]['main_info_id'],
			"composition" : sortedInfo
		})
	writeToFile(result, 'chemDataWithAllElements.txt')
	return result

# To do
def write_csv(filename, data):
    # with open (filename, 'w' ) as f:
	# 	fiiednames = ['1','2','3']
    #     writer = csv.Dictwriter(f, fieldnames=fieldnames)
	# 	writer.writeheader()
	with open (filename, 'w') as f:
		fieldnames = ['id','1','2', '3','4','5','6','7','8','9','10','11','12','13','14']
		writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator = '\n')
		writer.writeheader()

		for i in range(0, len(data)):
			writer.writerow({'id':data[i]['id'],'1': data[i]['composition'][0]['average'], '2': data[i]['composition'][1]['average'], '3':data[i]['composition'][2]['average'], '4':data[i]['composition'][3]['average'], '5':data[i]['composition'][4]['average'], '6':data[i]['composition'][5]['average'], '7':data[i]['composition'][6]['average'],'8':data[i]['composition'][7]['average'], '9':data[i]['composition'][8]['average'], '10':data[i]['composition'][9]['average'], '11':data[i]['composition'][10]['average'], '12':data[i]['composition'][11]['average'], '13':data[i]['composition'][12]['average'], '14':data[i]['composition'][13]['average']})

def write_to_db(data):
	conn = getConn()
	cur = conn.cursor()
	cur.execute("TRUNCATE TABLE rloveshhenko$mydbtest.composed_data")
	conn.commit()
	for elem in data:
		try:
			cur.execute("INSERT INTO rloveshhenko$mydbtest.composed_data VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (elem['id'], elem['composition'][0]['average'],elem['composition'][1]['average'],elem['composition'][2]['average'],elem['composition'][3]['average'],elem['composition'][4]['average'],elem['composition'][5]['average'],elem['composition'][6]['average'],elem['composition'][7]['average'],elem['composition'][8]['average'],elem['composition'][9]['average'],elem['composition'][10]['average'],elem['composition'][11]['average'],elem['composition'][12]['average'],elem['composition'][13]['average'],elem['composition'][14]['average'],elem['composition'][15]['average'],elem['composition'][16]['average'],elem['composition'][17]['average'],elem['composition'][18]['average'],elem['composition'][19]['average'],elem['composition'][20]['average'],elem['composition'][21]['average'],elem['composition'][22]['average'],elem['composition'][23]['average'],elem['composition'][24]['average'],elem['composition'][25]['average'],elem['composition'][26]['average'],elem['composition'][27]['average'],elem['composition'][28]['average'],elem['composition'][29]['average'],elem['composition'][30]['average'],elem['composition'][31]['average'],elem['composition'][32]['average'],elem['composition'][33]['average'],elem['composition'][34]['average'],elem['composition'][35]['average'],elem['composition'][36]['average'],elem['composition'][37]['average'],elem['composition'][38]['average'],elem['composition'][39]['average'],elem['composition'][40]['average'],elem['composition'][41]['average'],elem['composition'][42]['average'],elem['composition'][43]['average'],elem['composition'][44]['average'],elem['composition'][45]['average'],elem['composition'][46]['average'],elem['composition'][47]['average'],elem['composition'][48]['average'],elem['composition'][49]['average'],elem['composition'][50]['average'],elem['composition'][51]['average'],elem['composition'][52]['average'],elem['composition'][53]['average'],elem['composition'][54]['average'],elem['composition'][55]['average'],elem['composition'][56]['average'],elem['composition'][57]['average'],elem['composition'][58]['average'],elem['composition'][59]['average'],elem['composition'][60]['average'],elem['composition'][61]['average'],elem['composition'][62]['average'],elem['composition'][63]['average'],elem['composition'][64]['average'],elem['composition'][65]['average'],elem['composition'][66]['average'],elem['composition'][67]['average'],elem['composition'][68]['average'],elem['composition'][69]['average'],elem['composition'][70]['average'],elem['composition'][71]['average'],elem['composition'][72]['average'],elem['composition'][73]['average'],elem['composition'][74]['average'],elem['composition'][75]['average'],elem['composition'][76]['average'],elem['composition'][77]['average'],elem['composition'][78]['average'],elem['composition'][79]['average'],elem['composition'][80]['average'],elem['composition'][81]['average'],elem['composition'][82]['average'],elem['composition'][83]['average'],elem['composition'][84]['average'],elem['composition'][85]['average'],elem['composition'][86]['average'],elem['composition'][87]['average'],elem['composition'][88]['average'],elem['composition'][89]['average'],elem['composition'][90]['average'],elem['composition'][91]['average'],elem['composition'][92]['average'],elem['composition'][93]['average'],elem['composition'][94]['average'],elem['composition'][95]['average'],elem['composition'][96]['average'],elem['composition'][97]['average'],elem['composition'][98]['average'],elem['composition'][99]['average'],elem['composition'][100]['average'],elem['composition'][101]['average'],elem['composition'][102]['average'],elem['composition'][103]['average'],elem['composition'][104]['average'],elem['composition'][105]['average'],elem['composition'][106]['average'],elem['composition'][107]['average'],elem['composition'][108]['average'],elem['composition'][109]['average'],elem['composition'][110]['average'],elem['composition'][111]['average'],elem['composition'][112]['average'],elem['composition'][113]['average'],elem['composition'][114]['average'],elem['composition'][115]['average'],elem['composition'][116]['average'],elem['composition'][117]['average']))
			conn.commit()
		except Exception as e:
			print (str(e))
			continue;
	conn.close()

def composeDataForVisualization():

	#data = loadFromFile('chemDataWithAllElements.txt')
	# write_csv('data.csv',data)
	write_to_db(getChemicalCompositionData())

@app.route('/visualization')
def pygalexample():

	# print (data)
	# composeDataForChart()
	#data = loadFromFile('chemDataWithAllElements.txt')
	# for d in data:
	# 	print(d['composition'][25]['atomic_Number'])
	try:
		# startTime = time.time()
		# data = []
		# data2 = []
		# averages = get_averages_for_chart_C()
		# sigmas = get_sigma_t_for_chart_C()
		# for i in range (0, len(averages)):
		# 	data.append((float(averages[i]), float(sigmas[i])))
        #
		# averages = get_averages_for_chart_Si()
		# sigmas = get_sigma_t_for_chart_Si()
		# for i in range (0, len(averages)):
		# 	data2.append((float(averages[i]), float(sigmas[i])))
		# finishTime = time.time()
		# f = open('text.txt', 'w')
		# for index in data:
		# 	f.write(str(index) + '\n')
		# f.close()


		# result = composeDataForChart()
		# try to load it from file
		# result = loadFromFile('chartData.txt')

		result = loadFromFile('chartData.txt')
		# app.logger.info('Time Spent for gathering DATA ' + str(finishTime - startTime))
		# app.logger.info('DATA TO GRAPH length: ' + str(len(data)))
		from pygal.style import DarkStyle
		xy_chart = pygal.XY(stroke=False)
		#xy_chart.title = 'Dependence of the yield stress on the concentration of a chemical element'
		xy_chart.title = ''
		xy_chart.add('Silicium (Si)', result['data2'])
		xy_chart.add('Carboneum (С)', result['data1'])
		#xy_chart.add('B', [(.1, .15), (.12, .23), (.4, .3), (.6, .4), (.21, .21), (.5, .3), (.6, .8), (.7, .8)])
		#xy_chart.add('C', [(.05, .01), (.13, .02), (1.5, 1.7), (1.52, 1.6), (1.8, 1.63), (1.5, 1.82), (1.7, 1.23), (2.1, 2.23), (2.3, 1.98)])
		graph_data = xy_chart.render_data_uri()
		return render_template('pygal.html', graph_data = graph_data, title='Зависимость предела текучести для остаточной деформации от концентрации химического элемента для сталей:')
	except	Exception as e:
		return (str(e))

# Index
# @app.route('/')
# def index():
# 	return render_template('home.html')
sys.path.append('./routes')
from routes.static_pages import index_page, about_page
app.register_blueprint(index_page)
app.register_blueprint(about_page)


# # About
# @app.route('/about')
# def about():
# 	return render_template('about.html')

# Articles
@app.route('/articles')
def articles():
	conn = getConn()
	cur = conn.cursor()
	result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.articles")

	articles = cur.fetchall()
	cur.close()
	if result > 0:
		return render_template('articles.html', articles = articles)
	else:
		msg = 'No Articles Found'
		return render_template('articles.html', msg = msg)

# Single Article
@app.route('/article/<string:id>/')
def article(id):
	conn = getConn()
	cur = conn.cursor()

	result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.articles WHERE id = %s", [id])

	article = cur.fetchone()
	cur.close()

	return render_template('article.html', article = article)



#RegisterForm class
class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min = 1, max = 50)])
	username = StringField('Username', [validators.Length(min = 4, max = 25)])
	email = StringField('Email', [validators.Length(min = 6, max = 50)])
	password = PasswordField('Password',[
		validators.DataRequired(),
		validators.EqualTo('confirm', message = 'Passwords do not match')
	])
	confirm = PasswordField('Confirm Password')

# Register
@app.route('/register', methods = ['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		email = form.email.data
		username = form.username.data
		password = sha256_crypt.encrypt(str(form.password.data))

		#Create cursor
		conn = getConn()
		cur = conn.cursor()
		#Execute query
		user_result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.users WHERE username = %s", [username])
		if user_result > 0:
			flash('User already exist!', 'danger')
			return render_template('register.html', form = form)
		else:
			cur.execute("INSERT INTO rloveshhenko$mydbtest.users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
			#Commit to DB
			conn.commit()
		#Close the connection
		cur.close()

		flash('You are now registered and can log in', 'success')
		return redirect(url_for('index'))

	return render_template('register.html', form = form)
@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		#Ger form fields
		username = request.form['username']
		password_candidate = request.form['password']
		#Create cursor
		conn = getConn()
		cur = conn.cursor()
		#Get user by username
		result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.users WHERE username = %s", [username])

		if result > 0:
			#Get stored hash
			data = cur.fetchone()
			password = data['password']
			#Compare passwords
			if sha256_crypt.verify(password_candidate, password):
				session['logged_in'] = True
				session['username'] = username

				flash('You are now logged in', 'success')
				return redirect(url_for('materials', num = 1))

			else:
				flash('Invalid login', 'danger')
				return 	redirect(url_for('login'))

		else:
			flash('Username not found', 'danger')
			return 	redirect(url_for('login'))
		cur.close()
	return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Unauthorized, Please login', 'danger')
			return 	redirect(url_for('login'))
	return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash('You are now logged out', 'info')
	return redirect(url_for('login'))
# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
	conn = getConn()
	cur = conn.cursor()
	username = session['username']
	result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.articles WHERE author = %s", [username])

	articles = cur.fetchall()
	cur.close()
	if result > 0:
		return render_template('dashboard.html', articles = articles)
	else:
		msg = 'No Articles Found'
		return render_template('dashboard.html', msg = msg)


# Article Form class
class ArticleForm(Form):
	title = StringField('Title', [validators.Length(min = 1, max = 200)])
	body = TextAreaField('Body', [validators.Length(min = 40)])

@app.route('/add_article/', methods = ['GET', 'POST'])
@is_logged_in
def add_article():
	form = ArticleForm(request.form)
	if request.method == 'POST' and form.validate():
		title = form.title.data
		body = form.body.data

		conn = getConn()
		cur = conn.cursor()
		cur.execute("INSERT INTO rloveshhenko$mydbtest.articles(title,body,author) VALUES(%s, %s, %s)", (title,body,session['username']))
		conn.commit()
		cur.close()
		flash('Article Created', 'success')
		return redirect(url_for('dashboard'))
	return render_template('add_article.html', form = form)

# Edit article
@app.route('/edit_article/<string:id>', methods = ['GET', 'POST'])
@is_logged_in
def edit_article(id):
	conn = getConn()
	cur = conn.cursor()
	result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.articles WHERE id = %s and author=%s", (id,session['username']))
	article = cur.fetchone()
	if (not article):
		flash('Permission denied', 'danger')
		return redirect(url_for('dashboard'))
	# Get form
	form = ArticleForm(request.form)
	# Populate form fields
	form.title.data = article['title']
	form.body.data = article['body']

	if request.method == 'POST' and form.validate():
		title = request.form['title']
		body = request.form['body']
		# DB cursor
		conn = getConn()
		cur = conn.cursor()
		result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.articles WHERE id = %s and author=%s", (id,session['username']))
		article = cur.fetchone()
		if (not article):
			flash('Permission denied', 'danger')
			return redirect(url_for('dashboard'))
		cur.execute("UPDATE rloveshhenko$mydbtest.articles SET title = %s, body = %s WHERE id = %s", (title, body, id))
		conn.commit()
		cur.close()
		flash('Article Updated', 'success')
		return redirect(url_for('dashboard'))
	return render_template('edit_article.html', form = form)

# Delete article
@app.route('/delete_article/<string:id>', methods = ['POST'])
@is_logged_in
def delete_article(id):
	# Delete from DB
	conn = getConn()
	cur = conn.cursor()
	result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.articles WHERE id = %s and author=%s", (id,session['username']))
	article = cur.fetchone()
	if (not article):
		flash('Permission denied', 'danger')
		return redirect(url_for('dashboard'))
	cur.execute("DELETE FROM rloveshhenko$mydbtest.articles WHERE id = %s", [id])
	conn.commit()
	cur.close()
	flash('Article Deleted', 'success')
	return redirect(url_for('dashboard'))

# Materials
MATERIALS_PER_PAGE = 50
@app.route('/materials/', defaults={'num': 1})
@app.route('/materials/page/<int:num>')
def materials(num):
	app.config['MYSQL_DB'] = 'mydbtest'
	conn = getConn()
	cur = conn.cursor()
	total = cur.execute("SELECT * FROM rloveshhenko$mydbtest.main_info")
	#print (total)
	total_page = (int)(total / MATERIALS_PER_PAGE) + 1
	#print (total_page)
	result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.main_info limit %s,%s", ((num-1)*MATERIALS_PER_PAGE, MATERIALS_PER_PAGE))

	#print ((num-1)*MATERIALS_PER_PAGE)
	if result > 0:
		materials = cur.fetchall()
		cur.close()
		return render_template('materials.html', materials = materials, page = num, total = total_page)
	else:
		msg = 'No Materials Found'
		cur.close()
		return render_template('materials.html', msg = msg)

# Material
@app.route('/material/<string:id>')
def material(id):
	# Creating cursor and getting main info about material
	app.config['MYSQL_DB'] = 'mydbtest'
	conn = getConn()
	cur = conn.cursor()
	result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.main_info WHERE id = %s", [id])
	material = cur.fetchone()

	# Getting chemical composition
	result_chem = cur.execute("SELECT * FROM rloveshhenko$mydbtest.chemical_composition WHERE main_info_id = %s", [id])
	chem_composition = cur.fetchall()
	chem_elem = []
	chem_concetration = []

	if result_chem > 0:
		for number in chem_composition:
			chem_concetration.append(number['concetration'])
		for number in chem_composition:
			if number['atomic_Number'] == -1:
				chem_elem.append('Примесей')
			else:
				cur.execute("SELECT * FROM rloveshhenko$mydbtest.periodic_table WHERE atomic_Number = %s", [number['atomic_Number']])
				data = cur.fetchone()
				chem_elem.append(data['symbol'])

	#print (chem_elem)
	#print (chem_concetration)

	# Getting critical temperature
	result_crit = cur.execute("SELECT * FROM rloveshhenko$mydbtest.critical_temperature WHERE main_info_id = %s", [id])
	critical_temperature = cur.fetchone()

	# Getting techno properties
	result_techno = cur.execute("SELECT * FROM rloveshhenko$mydbtest.techno_properties WHERE main_info_id = %s", [id])
	techno = cur.fetchall()

	# Getting termo-mode
	result_termo_mode = cur.execute("SELECT * FROM rloveshhenko$mydbtest.termo_mode WHERE main_info_id = %s", [id])
	termo_mode = cur.fetchall()

	# Getting mechanical properties
	result_mech = cur.execute("SELECT * FROM rloveshhenko$mydbtest.mechanical_properties WHERE main_info_id = %s", [id])
	mech = cur.fetchall()

	# Getting table6 (DELETE SPACES - TOO MUCH)
	result_table6 = cur.execute("SELECT * FROM rloveshhenko$mydbtest.table6 WHERE main_info_id = %s", [id])
	table6 = cur.fetchall()

	# Getting physical properties
	result_physic =  cur.execute("SELECT * FROM rloveshhenko$mydbtest.physical_properties WHERE main_info_id = %s", [id])
	physic = cur.fetchall()

	cur.close()


	if result > 0:
		return render_template('material.html', material = material, elements = chem_elem, concetration = chem_concetration,
		critical_temperature = critical_temperature, techno = techno, termo_mode = termo_mode, mech = mech, table6 = table6, physic = physic)
	else:
		msg = 'Material Doesnt Exist'
		return  redirect(url_for('materials'))

# Default search by name
@app.route('/search', methods = ['POST'])
def default_search():
	if request.method == 'POST':
		name = request.form['mat_name']
		conn = getConn()
		cur = conn.cursor()
		total = cur.execute("SELECT * FROM rloveshhenko$mydbtest.main_info WHERE marka like %s or marka = %s", ("%" + name + "%","%" + name + "%"))
		materials = cur.fetchall()
		cur.close()
		return render_template('default_search.html', materials = materials, name = name)

# Compare to materials via their chemical compositons
# Return index of similarity
def simple_Compare(chem_composition_first,chem_composition_second):
	sum = 0
	sum_container = []
	element_container = []

	for chem_2 in chem_composition_second:

		for chem_1 in chem_composition_first:

			if (chem_2['atomic_Number'] == chem_1['atomic_Number']):
				sum_container.append((chem_1['average'] - chem_2['average']) ** 2)
				element_container.append(chem_1['atomic_Number'])
				break

	for chem_1 in chem_composition_first:
		if (chem_1['atomic_Number'] not in element_container):
			sum_container.append((chem_1['average']) ** 2)

	for chem_2 in chem_composition_second:
		if (chem_2['atomic_Number'] not in element_container):
			sum_container.append((chem_2['average']) ** 2)

	for el in sum_container:
		sum += el

	index = math.sqrt(sum)
	return index

def chemical_Compare(chem_composition_first, chemical_composition_others, other_materials, cur):

	return 0




def getChemicalComposition(id,chem_composition_others):
	chem_composition = []
	for material in chem_composition_others:
		if material['main_info_id'] == id:
			chem_composition.append(material)
	return chem_composition


def getKey(material):
    return material['index']

@app.route('/chemical_search/<int:id>', methods = ['POST', 'GET'])
def chemical_search(id):
	conn = getConn()
	cur = conn.cursor()
	name_res = cur.execute("SELECT * FROM rloveshhenko$mydbtest.main_info where id = %s", [id])
	base_material = cur.fetchone()


	result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.main_info where id != %s", [id])
	other_materials = cur.fetchall()

	result_first = cur.execute("SELECT atomic_Number, average FROM rloveshhenko$mydbtest.chemical_composition WHERE main_info_id = %s", [id])
	chem_composition_first = cur.fetchall()

	result_others = cur.execute("SELECT main_info_id, atomic_Number, average FROM rloveshhenko$mydbtest.chemical_composition WHERE main_info_id != %s", [id])
	chem_composition_others = cur.fetchall()

	app.logger.info('Other materials: ' + str(result))
	startTime = time.time()

	#indexes = chemical_Compare(chem_composition_first, chem_composition_others, other_materials, cur)
	for mat in other_materials:
		mat['index'] = simple_Compare(chem_composition_first, getChemicalComposition(mat['id'], chem_composition_others))
	"""for material in other_materials:
		material['index'] = chemical_Compare(chem_composition_first, material['id'], cur)"""

	finishTime = time.time()
	print(other_materials[-1])
	res = sorted(other_materials, key=getKey)
	print(res[-1])
	cur.close()
	app.logger.info('Time spent: ' + str(finishTime - startTime))
	return render_template('chemSimilar.html', materials = res, base_material = base_material)

	#return redirect(url_for('material', id = id))


# Main Part
if __name__ == '__main__':
	app.secret_key = 'secret123'
	app.run(debug=True)
