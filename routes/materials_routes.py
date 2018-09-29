import sys

from flask import Blueprint, render_template, redirect, url_for

sys.path.append('../')
from services.mysql_service import getConnection

sys.path.remove('../')

sys.path.append('./config')
import config
sys.path.remove('./config')

materials = Blueprint('materials', __name__,template_folder='templates')

# Materials
@materials.route('/materials/', defaults={'num': 1})
@materials.route('/materials/page/<int:num>')
def allMaterials(num):
	conn = getConnection()
	cur = conn.cursor()
	total = cur.execute("SELECT * FROM rloveshhenko$mydbtest.main_info")
	#print (total)
	total_page = (int)(total / config.MATERIALS_PER_PAGE) + 1
	#print (total_page)
	result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.main_info limit %s,%s", ((num-1)* config.MATERIALS_PER_PAGE, config.MATERIALS_PER_PAGE))

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
@materials.route('/material/<string:id>')
def singleMaterial(id):
	conn = getConnection()
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