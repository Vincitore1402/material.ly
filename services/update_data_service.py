from utils.chemical_utils import getDataForLearning, composeDataForChart
from utils.common_utils import writeDataToFile
from services.sckit_learn import startManifoldLearning

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
