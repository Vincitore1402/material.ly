from flask import current_app

from services.mysql_service import MySQLService

from pydash import map_

db = MySQLService()

class FixDBService():
	def fix_sigma_t_dashes(self):
		conn = db.getConnection()
		cur = conn.cursor()
		SELECT_DASHES_SIGMAS_QUERY = 'SELECT id, sigma_t FROM rloveshhenko$mydbtest.mechanical_properties WHERE sigma_t LIKE "%-%";'
		cur.execute(SELECT_DASHES_SIGMAS_QUERY)
		data = cur.fetchall()

		res = map_(data,
			lambda item: { 'id': item['id'], 'new_sigma' :
				(float(item['sigma_t'].split('-')[0]) + float(item['sigma_t'].split('-')[1]))/2
			}
		)
		current_app.logger.info('Started fixing dashed SIGMA_T...')
		for item in res:
			cur.execute('UPDATE rloveshhenko$mydbtest.mechanical_properties SET sigma_t = %s WHERE id = %s', (item['new_sigma'], item['id']))
			conn.commit()
		cur.close()
		current_app.logger.info('SIGMA_T fixed!')
		return True