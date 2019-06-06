from flask import Blueprint, render_template, redirect, url_for

from services.mysql_service import MySQLService

from utils.common_utils import get_config

import json

config = get_config()

db = MySQLService()

materials = Blueprint('materials', __name__, template_folder='templates')


# Materials
@materials.route('/materials/', defaults={'num': 1})
@materials.route('/materials/page/<int:num>')
def all_materials(num):
	result = db.get_all_materials(num, config.MATERIALS_PER_PAGE)
	materials = result[0]
	total_page = result[1]

	if len(materials) > 0:
		return render_template('materials.html', materials=materials, page=num, total=total_page)
	else:
		msg = 'No Materials Found'
		return render_template('materials.html', msg=msg)


# Material
@materials.route('/material/<string:id>')
def single_material(id):
	conn = db.get_connection()
	cur = conn.cursor()
	result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.main_info WHERE id = %s", [id])
	material = cur.fetchone()

	# Getting chemical composition
	result_chem = cur.execute("SELECT * FROM rloveshhenko$mydbtest.chemical_composition WHERE main_info_id = %s", [id])
	chem_composition = cur.fetchall()
	chem_elem = []
	chem_concentration = []

	if result_chem > 0:
		for number in chem_composition:
			chem_concentration.append(number['concetration'])
		for number in chem_composition:
			if number['atomic_Number'] == -1:
				chem_elem.append('Примесей')
			else:
				cur.execute("SELECT * FROM rloveshhenko$mydbtest.periodic_table WHERE atomic_Number = %s",
				            [number['atomic_Number']])
				data = cur.fetchone()
				chem_elem.append(data['symbol'])

	print(chem_elem)
	print(chem_concentration)

	# getting number from chem_concetration
	chem_concetration_number = [0 for i in range(chem_concentration.__len__())]

	for i in range(chem_concentration.__len__()):
		for t in chem_concentration[i].split():
			try:
				chem_concetration_number[i] = float(t)
			except ValueError:
				pass

	print(chem_concetration_number)
	# Getting critical temperature
	cur.execute("SELECT * FROM rloveshhenko$mydbtest.critical_temperature WHERE main_info_id = %s", [id])
	critical_temperature = cur.fetchone()
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
	result_physic = cur.execute("SELECT * FROM rloveshhenko$mydbtest.physical_properties WHERE main_info_id = %s", [id])
	physic = cur.fetchall()

	cur.close()

	if result > 0:
		return render_template('material.html', material=material, elements=chem_elem, concetration=chem_concentration,
		                       critical_temperature=critical_temperature, techno=techno, termo_mode=termo_mode, mech=mech,
		                       table6=table6, physic=physic,
		                       chem_elem=json.dumps(chem_elem),
		                       chem_concetration_number=json.dumps(chem_concetration_number), length=chem_elem.__len__())
	else:
		return redirect(url_for('materials'))
