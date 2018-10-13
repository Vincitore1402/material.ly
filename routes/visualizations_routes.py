from flask import Blueprint, render_template, current_app

from utils.common_utils import loadDataFromFile
from services.pygal_service import PygalService

pygalService = PygalService()

visualization = Blueprint('visualization', __name__,template_folder='templates')

@visualization.route('/visualization/yield_strength')
def yield_strength():
	try:
		# result = composeDataForChart()
		# try to load it from file
		# result = loadFromFile('chartData.txt')

		result = loadDataFromFile('chartData.txt')
		data = {
			'Silicium (Si)': result['data2'],
			'Carboneum (С)': result['data1']
		}

		graph_data = pygalService.createXYChart(data)

		return render_template('pygal.html', graph_data = graph_data, title='Зависимость предела текучести для остаточной деформации от концентрации химического элемента для сталей:')
	except	Exception as e:
		return (str(e))


@visualization.route('/visualization/manifold_learning')
def manifold_learning():
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

	# pygal_manif = []
	# for key, value in manif.items():
	# 	res = []
	# 	for i in range(0, len(value['x'])):
	# 		res.append({'value': [value['x'][i],value['y'][i]], 'label': str(value['matInfo'][i])})
	# 	pygal_manif.append((key, res))
	# 	# xy_chart.add(key, res)

	# writeToFile(pygal_manif, 'manifPygal.txt')

	data = loadDataFromFile('manifPygal.txt')
	for item in data:
		if (item[0] == 'Spectral Embedding'):
			data.remove(item)

	graph_data = pygalService.createXYChart(data)

	return render_template('pygal.html', graph_data=graph_data)