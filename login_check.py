from flask import flash, redirect, url_for, session
from functools import wraps

# Check if user logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Unauthorized, Please login', 'danger')
			return 	redirect(url_for('login'))
	return wrap