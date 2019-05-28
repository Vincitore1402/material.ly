from flask import Blueprint, render_template, abort, session, redirect, url_for
from jinja2 import TemplateNotFound


index_page = Blueprint('index_page', __name__,template_folder='templates')
about_page = Blueprint('about_page', __name__,template_folder='templates')

@index_page.route('/')
def index():
  try:
    return render_template('home.html')

  except TemplateNotFound:
    abort(404)

@index_page.route('/ADMIN')
def ADMIN():
  return redirect(url_for('admin.index'))


@about_page.route('/about')
def about():
  try:
    return render_template('about.html')
  except TemplateNotFound:
    abort(404)
