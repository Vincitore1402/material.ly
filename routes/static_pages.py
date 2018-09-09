from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

index_page = Blueprint('index_page', __name__,template_folder='templates')
about_page = Blueprint('about_page', __name__,template_folder='templates')

@index_page.route('/')
def index():
  try:
    return render_template('home.html')
  except TemplateNotFound:
    abort(404)

@about_page.route('/about')
def about():
  try:
    return render_template('about.html')
  except TemplateNotFound:
    abort(404)