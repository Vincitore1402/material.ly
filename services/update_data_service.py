from utils.chemical_utils import get_data_for_learning, compose_data_for_chart
from utils.common_utils import write_data_to_file
from services.sckit_learn import start_manifold_learning, start_regression_learning
from services.mysql_service import MySQLService
from pydash import map_, filter_, reduce_, get

import numpy as np

db = MySQLService()


def extract_x(item):
  return np.array(list(dict(item).values())[1:-1]).astype(float)


def extract_y(item):
  return np.array(list(dict(item).values())[-1:]).astype(float)


class UpdateGraphDataService:
  @staticmethod
  def update_manifold_learning_data():
    input = get_data_for_learning()
    manifold_data = start_manifold_learning(input)

    data = []
    for key, value in manifold_data.items():
      res = []
      for i in range(0, len(value['x'])):
        res.append({'value': [value['x'][i], value['y'][i]], 'label': str(value['matInfo'][i])})
      data.append((key, res))

    write_data_to_file(data, 'manifPygal.txt')

  @staticmethod
  def update_yield_strength_data():
    data = compose_data_for_chart()
    write_data_to_file(data, 'chartData.txt')

  @staticmethod
  def update_yield_strength_regression_data():
    conn = db.get_connection()
    cur = conn.cursor()
    sql_select = "SELECT * FROM rloveshhenko$mydbtest.composed_data"
    cur.execute(sql_select)
    data = cur.fetchall()

    x = np.array(map_(data, extract_x))
    y = np.array(map_(data, extract_y))

    data = {
      'x': x,
      'y': y
    }

    # 'ndarray' is not JSON serializable
    # writeDataToFile(data, 'regressionData.txt')

    start_regression_learning(data)


# TODO refactor

class GetComposedDataService:
  @staticmethod
  def get_yield_strength_to_composed_data():
    conn = db.get_connection()
    cur = conn.cursor()
    main_query_select = 'SELECT main_info_id, sortament, sigma_t FROM rloveshhenko$mydbtest.mechanical_properties WHERE sigma_t != " " and main_info_id in (SELECT id FROM mydbtest.main_info WHERE classification like "%Сталь%");'

    ids_query_select = 'SELECT distinct main_info_id FROM rloveshhenko$mydbtest.mechanical_properties WHERE sigma_t != " " and main_info_id in (SELECT id FROM mydbtest.main_info WHERE classification like "%Сталь%");'

    cur.execute(main_query_select)
    data = cur.fetchall()
    cur.execute(ids_query_select)
    ids = cur.fetchall()

    sigmas = map_(ids,
                  lambda item:
                  {'id': item['main_info_id'], 'sigmas': map_(filter_(data,
                                                                      lambda it:
                                                                      it['main_info_id'] == item['main_info_id']),
                                                              lambda x: get(x, 'sigma_t'))}
                  )

    new_sigmas = map_(sigmas,
                      lambda item:
                      {'id': item['id'], 'sigma': format(
                        reduce_(item['sigmas'], lambda total, x: float(total) + float(x) / len(item['sigmas']), 0),
                        '.2f')}
                      )

    for item in new_sigmas:
      cur.execute("UPDATE rloveshhenko$mydbtest.composed_data SET sigma_t = %s WHERE id = %s",
                  (item['sigma'], item['id']))
      conn.commit()

    cur.close()
    return True
