from services.mysql_service import MySQLService
from utils.common_utils import is_logged_in

from flask import Blueprint, render_template, session

dashboard_route = Blueprint('dashboard_route', __name__, template_folder='templates')

db = MySQLService()


@dashboard_route.route('/dashboard')
@is_logged_in
def dashboard():
  username = session['username']

  articles = db.get_articles_by_author(username)

  if len(articles) > 0:
    return render_template('dashboard.html', articles=articles)
  else:
    msg = 'No Articles Found'
    return render_template('dashboard.html', msg=msg)
