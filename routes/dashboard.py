import sys

from flask import Blueprint, render_template, session

sys.path.append('../')
from services.mysql_service import getConnection
from utils.common_utils import is_logged_in
sys.path.remove('../')

dashboard_route = Blueprint('dashboard_route', __name__,template_folder='templates')

# Dashboard
@dashboard_route.route('/dashboard')
@is_logged_in
def dashboard():
	conn = getConnection()
	cur = conn.cursor()
	username = session['username']
	result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.articles WHERE author = %s", [username])

	articles = cur.fetchall()
	cur.close()
	if result > 0:
		return render_template('dashboard.html', articles = articles)
	else:
		msg = 'No Articles Found'
		return render_template('dashboard.html', msg = msg)