from utils.chemical_utils import getDataForLearning, composeDataForChart
from utils.common_utils import writeDataToFile
from services.sckit_learn import startManifoldLearning, startRegressionLearning
from services.mysql_service import MySQLService

from pydash import map_, filter_, reduce_, get
import numpy as np

db = MySQLService()

class UpdateGraphDataService():
	def updateManifoldLearningData(self):
		input = getDataForLearning()
		manifold_data = startManifoldLearning(input)

		data = []
		for key, value in manifold_data.items():
			res = []
			for i in range(0, len(value['x'])):
				res.append({'value': [value['x'][i],value['y'][i]], 'label': str(value['matInfo'][i])})
			data.append((key, res))

		writeDataToFile(data, 'manifPygal.txt')

	def updateYieldStrengthData(self):
		data = composeDataForChart()
		writeDataToFile(data, 'chartData.txt')

	def updateYieldStrengthRegressionData(self):
		conn = db.getConnection()
		cur = conn.cursor()
		SQL_SELECT = "SELECT * FROM rloveshhenko$mydbtest.composed_data"
		SQL_SELECT_INFO = "SELECT classification,marka FROM rloveshhenko$mydbtest.main_info WHERE id in (SELECT id FROM rloveshhenko$mydbtest.composed_data)"
		cur.execute(SQL_SELECT)
		data = cur.fetchall()
		cur.execute(SQL_SELECT_INFO)
		info = cur.fetchall()

		arrayData = []
		ids = []
		for d in data:
			arr = np.array(list(dict(d).values())[1:]).astype(float)
			arrayData.append(arr)
			ids.append(list(dict(d).values())[:1][0])

		matInfo = []

		for i in info:
			listInfo = list(dict(i).values())
			matInfo.append(str(listInfo[0]) + " " + str(listInfo[1]))
		npArr = np.array(arrayData)

		input =  {
			'numpyArr': npArr,
			'matInfo': matInfo,
			'ids': ids
		}

		# todo
		# result = startRegressionLearning(input)
		#writeDataToFile(result, '....')

class GetComposedDataService():
	def getYieldStrengthToComposedData(self):
		conn = db.getConnection()
		cur = conn.cursor()
		MAIN_QUERY_SELECT = 'SELECT main_info_id, sortament, sigma_t FROM rloveshhenko$mydbtest.mechanical_properties WHERE sigma_t != " " and main_info_id in (SELECT id FROM mydbtest.main_info WHERE classification like "%Сталь%");'

		IDS_QUERY_SELECT = 'SELECT distinct main_info_id FROM rloveshhenko$mydbtest.mechanical_properties WHERE sigma_t != " " and main_info_id in (SELECT id FROM mydbtest.main_info WHERE classification like "%Сталь%");'

		cur.execute(MAIN_QUERY_SELECT)
		data = cur.fetchall()
		cur.execute(IDS_QUERY_SELECT)
		ids = cur.fetchall()

		sigmas = map_(ids,
			lambda item:
				{'id': item['main_info_id'], 'sigmas': map_(filter_(data,
					lambda it:
						it['main_info_id'] == item['main_info_id'] ), lambda x : get(x, 'sigma_t')) }
		)

		new_sigmas = map_(sigmas,
			lambda item:
				{ 'id': item['id'], 'sigma': format(reduce_(item['sigmas'], lambda total, x: float(total) + float(x)/len(item['sigmas']), 0), '.2f') }
		)

		for item in new_sigmas:
			cur.execute("UPDATE rloveshhenko$mydbtest.composed_data SET sigma_t = %s WHERE id = %s", (item['sigma'], item['id']))
			conn.commit()

		cur.close()
		return True