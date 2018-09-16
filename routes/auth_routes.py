from flask import Blueprint, render_template, abort, request, session, flash, redirect, url_for
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

import sys
sys.path.append('../')
from db import getConnection
from login_check import is_logged_in
sys.path.remove('../')

register = Blueprint('register', __name__,template_folder='templates')
login = Blueprint('login', __name__,template_folder='templates')
logout = Blueprint('logout', __name__,template_folder='templates')

#RegisterForm class
class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min = 1, max = 50)])
	username = StringField('Username', [validators.Length(min = 4, max = 25)])
	email = StringField('Email', [validators.Length(min = 6, max = 50)])
	password = PasswordField('Password',[
		validators.DataRequired(),
		validators.EqualTo('confirm', message = 'Passwords do not match')
	])
	confirm = PasswordField('Confirm Password')

# Register
@register.route('/register', methods = ['GET', 'POST'])
def registerUser():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		email = form.email.data
		username = form.username.data
		password = sha256_crypt.encrypt(str(form.password.data))

		#Create cursor
		conn = getConnection()
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
		return redirect(url_for('index'))

	return render_template('register.html', form = form)

@login.route('/login', methods = ['GET', 'POST'])
def logIn():
	if request.method == 'POST':
		#Ger form fields
		username = request.form['username']
		password_candidate = request.form['password']
		#Create cursor
		conn = getConnection()
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
				return 	redirect(url_for('login.logIn'))

		else:
			flash('Username not found', 'danger')
			return 	redirect(url_for('login.logIn'))
		cur.close()
	return render_template('login.html')

# Logout
@logout.route('/logout')
@is_logged_in
def logOut():
	session.clear()
	flash('You are now logged out', 'info')
	return redirect(url_for('login.logIn'))



