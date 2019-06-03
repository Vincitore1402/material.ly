from services.mysql_service import MySQLService
from utils.common_utils import is_logged_in
from models.User import User

from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from passlib.hash import sha256_crypt

from forms.forms import RegisterForm

auth = Blueprint('auth', __name__, template_folder='templates')

db = MySQLService()


@auth.route('/register', methods=['GET', 'POST'])
def register():
  form = RegisterForm(request.form)
  if request.method == 'POST' and form.validate():
    name = form.name.data
    email = form.email.data
    username = form.username.data
    # TODO
    password = sha256_crypt.encrypt(str(form.password.data))

    user = User(name, email, username, password)

    if db.register_user(user):
      flash('You are now registered and can log in', 'success')
      return redirect(url_for('index'))
    else:
      flash('User already exist!', 'danger')
      return render_template('register.html', form=form)

  return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    # Get form fields
    username = request.form['username']
    password_candidate = request.form['password']

    user = db.login(username, password_candidate)

    if user:
      session['logged_in'] = True
      session['username'] = username
      flash('You are now logged in', 'success')
      return redirect(url_for('materials.all_materials', num=1))
    else:
      flash('Invalid credentials', 'danger')
      return redirect(url_for('auth.login'))

  return render_template('login.html')


# Logout
@auth.route('/logout')
@is_logged_in
def logout():
  session.clear()
  flash('You are now logged out', 'info')
  return redirect(url_for('auth.login'))
