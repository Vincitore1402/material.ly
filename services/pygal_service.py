import pygal


class PygalService:
  @staticmethod
  def create_xy_chart(data, title=''):
    xy_chart = pygal.XY(stroke=False)
    xy_chart.title = title

    if type(data) is dict:
      for key, value in data.items():
        xy_chart.add(key, value)
    else:
      for item in data:
        xy_chart.add(item[0], item[1])

    # xy_chart.add('B', [{'value': [.1,.15], 'label': 'Some plain text here'}, (.12, .23), (.4, .3), (.6, .4), (.21, .21), (.5, .3), (.6, .8), (.7, .8)])
    # xy_chart.add('C', [(.05, .01), (.13, .02), (1.5, 1.7), (1.52, 1.6), (1.8, 1.63), (1.5, 1.82), (1.7, 1.23), (2.1, 2.23), (2.3, 1.98)])

    return xy_chart.render_data_uri()
