from flask import Blueprint
from services.mysql_service import MySQLService
import json

db = MySQLService()

api = Blueprint('api', __name__, template_folder='templates')

@api.route('/api/getMaterial/<string:id>')
def getMaterial(id):
    conn = db.getConnection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM rloveshhenko$mydbtest.main_info WHERE id = %s", [id])
    material = cur.fetchone()

    # Getting critical temperature
    cur.execute("SELECT * FROM rloveshhenko$mydbtest.critical_temperature WHERE main_info_id = %s", [id])
    critical_temperature = cur.fetchone()

    # Getting techno properties
    cur.execute("SELECT * FROM rloveshhenko$mydbtest.techno_properties WHERE main_info_id = %s", [id])
    techno = cur.fetchall()

    # Getting termo-mode
    cur.execute("SELECT * FROM rloveshhenko$mydbtest.termo_mode WHERE main_info_id = %s", [id])
    termo_mode = cur.fetchall()

    # Getting mechanical properties
    cur.execute("SELECT * FROM rloveshhenko$mydbtest.mechanical_properties WHERE main_info_id = %s", [id])
    mech = cur.fetchall()

    # Getting table6 (DELETE SPACES - TOO MUCH)
    cur.execute("SELECT * FROM rloveshhenko$mydbtest.table6 WHERE main_info_id = %s", [id])
    table6 = cur.fetchall()

    # Getting physical properties
    cur.execute("SELECT * FROM rloveshhenko$mydbtest.physical_properties WHERE main_info_id = %s", [id])
    physic = cur.fetchall()

    cur.close()

    data = {}
    data['Main'] = material
    data['Critical_temperature'] = critical_temperature
    data['Techno_properties'] = techno
    data['Termo_mode'] = termo_mode
    data['Mechanical_properties'] = mech
    data['Table6'] = table6
    data['Physical_properties'] = physic

    return json.dumps(data, ensure_ascii=False, indent=4, separators=(',', ': '))