import math
from utils.common_utils import writeDataToFile
from services.mysql_service import MySQLService
from flask import current_app as app
import numpy as np

db = MySQLService()

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

def getChemicalComposition(id,chem_composition_others):
	chem_composition = []
	for material in chem_composition_others:
		if material['main_info_id'] == id:
			chem_composition.append(material)
	return chem_composition

def getKey(material):
  return material['index']

# Function to sort tuple by atomic numbers
def getKeyForAtomicNumbers(item):
	return item['atomic_Number']

def get_sigma_t_for_chart_C():
	conn = db.getConnection()
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
	conn = db.getConnection()
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
	conn = db.getConnection()
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
	conn = db.getConnection()
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
	# writeDataToFile(result, 'chartData.txt')
	return result

# Manifold learning data part
def getDataForLearning():
	import numpy as np
	# Getting data from DB
	conn = db.getConnection()
	cur = conn.cursor()

	SQL_SELECT = "SELECT * FROM rloveshhenko$mydbtest.composed_data"
	SQL_SELECT_INFO = "SELECT classification,marka FROM rloveshhenko$mydbtest.main_info WHERE id in (SELECT id FROM rloveshhenko$mydbtest.composed_data)"

	cur.execute(SQL_SELECT)
	composed_data = cur.fetchall()

	# new composed_data in DB Fix
	# composed_data = composed_data[:,:-2]

	cur.execute(SQL_SELECT_INFO)
	info = cur.fetchall()

	arrayData = []
	ids = []
	for d in composed_data:
		# add [1:-1]
		arr = np.array(list(dict(d).values())[1:]).astype(float)
		arrayData.append(arr)
		ids.append(list(dict(d).values())[:1][0])

	matInfo = []

	for i in info:
		listInfo = list(dict(i).values())
		matInfo.append(str(listInfo[0]) + " " + str(listInfo[1]))
	npArr = np.array(arrayData)

	return {
		'numpyArr': npArr,
		'matInfo': matInfo,
		'ids': ids
	}

def writeComposedDataToDB(data):
	conn = db.getConnection()
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

def getChemicalCompositionData():
	conn = db.getConnection()
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
	writeDataToFile(result, '../chemDataWithAllElements.txt')
	return result

def composeDataForVisualization():

	#data = loadFromFile('chemDataWithAllElements.txt')
	# write_csv('data.csv',data)
	writeComposedDataToDB(getChemicalCompositionData())