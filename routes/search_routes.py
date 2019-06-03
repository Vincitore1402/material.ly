import time
from flask import Blueprint, render_template, request, current_app

from services.mysql_service import MySQLService
from utils.chemical_utils import simple_compare, get_chemical_composition, get_key

searches = Blueprint('searches', __name__, template_folder='templates')

db = MySQLService()


# Default search by name
@searches.route('/search', methods=['POST'])
def default_search():
  if request.method == 'POST':
    name = request.form['mat_name']
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM rloveshhenko$mydbtest.main_info WHERE marka like %s or marka = %s",
                ("%" + name + "%", "%" + name + "%"))
    materials = cur.fetchall()
    cur.close()
    return render_template('default_search.html', materials=materials, name=name)


@searches.route('/chemical_search/<int:id>', methods=['POST', 'GET'])
def chemical_search(id):
  conn = db.get_connection()
  cur = conn.cursor()
  cur.execute("SELECT * FROM rloveshhenko$mydbtest.main_info where id = %s", [id])
  base_material = cur.fetchone()

  result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.main_info where id != %s", [id])
  other_materials = cur.fetchall()

  cur.execute(
    "SELECT atomic_Number, average FROM rloveshhenko$mydbtest.chemical_composition WHERE main_info_id = %s", [id])
  chem_composition_first = cur.fetchall()

  cur.execute(
    "SELECT main_info_id, atomic_Number, average FROM rloveshhenko$mydbtest.chemical_composition WHERE main_info_id != %s",
    [id])
  chem_composition_others = cur.fetchall()

  current_app.logger.info('Other materials: ' + str(result))
  start_time = time.time()

  # indexes = chemical_Compare(chem_composition_first, chem_composition_others, other_materials, cur)
  for mat in other_materials:
    mat['index'] = simple_compare(chem_composition_first, get_chemical_composition(mat['id'], chem_composition_others))
  """for material in other_materials:
		material['index'] = chemical_Compare(chem_composition_first, material['id'], cur)"""

  finish_time = time.time()
  print(other_materials[-1])
  res = sorted(other_materials, key=get_key)
  print(res[-1])
  cur.close()
  current_app.logger.info('Time spent: ' + str(finish_time - start_time))
  return render_template('chemSimilar.html', materials=res, base_material=base_material)
