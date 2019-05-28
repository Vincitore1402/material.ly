import sys

from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from passlib.hash import sha256_crypt

from forms.forms import RegisterForm

sys.path.append('../')
from services.mysql_service import MySQLService
from utils.common_utils import is_logged_in
sys.path.remove('../')

auth = Blueprint('auth', __name__, template_folder='templates')

db = MySQLService()

# Register
@auth.route('/register', methods = ['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		email = form.email.data
		username = form.username.data
		password = sha256_crypt.encrypt(str(form.password.data))

		#Create cursor
		conn = db.getConnection()
		cur = conn.cursor()
		#Execute query
		user_result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.users WHERE username = %s", [username])
		if user_result > 0:
			flash('User already exist!', 'danger')
			return render_template('register.html', form = form)
		else:
			cur.execute("INSERT INTO rloveshhenko$mydbtest.users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
			#Commit to DB
			conn.commit()
		#Close the connection
		cur.close()

		flash('You are now registered and can log in', 'success')
		return redirect(url_for('index_page.index'))

	return render_template('register.html', form = form)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		#Ger form fields
		username = request.form['username']
		password_candidate = request.form['password']

		#Create cursor
		conn = db.getConnection()
		cur = conn.cursor()
		#Get user by username
		result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.users WHERE username = %s", [username])

		if result > 0:
			#Get stored hash
			data = cur.fetchone()
			password = data['password']
			#Compare passwords
			if sha256_crypt.verify(password_candidate, password):
				session['logged_in'] = True
				session['username'] = username

				flash('You are now logged in', 'success')
				return redirect(url_for('materials.allMaterials', num = 1))

			else:
				flash('Invalid login', 'danger')
				return 	redirect(url_for('auth.login'))

		else:
			flash('Username not found', 'danger')
			return 	redirect(url_for('auth.login'))
		cur.close()
	return render_template('login.html')

# Logout
@auth.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash('You are now logged out', 'info')
	return redirect(url_for('auth.login'))








