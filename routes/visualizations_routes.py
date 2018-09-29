import pygal
from flask import Blueprint, render_template

from utils.common_utils import loadDataFromFile

visualization = Blueprint('visualization', __name__,template_folder='templates')

@visualization.route('/visualization/yield_strength')
def yield_strength():
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

		result = loadDataFromFile('chartData.txt')
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
	pygal_manif = loadDataFromFile('manifPygal.txt')
	for item in pygal_manif:
		if (item[0] == 'Spectral Embedding'):
			continue
		xy_chart.add(item[0], item[1])
		print(item[0] + " :" + str(len(item[1])))

	# xy_chart.title = 'Dependence of the yield stress on the concentration of a chemical element'
	xy_chart.title = ''
	# xy_chart.add('Spectral Embedding', res)
	# xy_chart.add('Carboneum (С)', result['data1'])
	# xy_chart.add('B', [{'value': [.1,.15], 'label': 'Some plain text here'}, (.12, .23), (.4, .3), (.6, .4), (.21, .21), (.5, .3), (.6, .8), (.7, .8)])
	# xy_chart.add('C', [(.05, .01), (.13, .02), (1.5, 1.7), (1.52, 1.6), (1.8, 1.63), (1.5, 1.82), (1.7, 1.23), (2.1, 2.23), (2.3, 1.98)])
	graph_data = xy_chart.render_data_uri()
	return render_template('pygal.html', graph_data=graph_data)