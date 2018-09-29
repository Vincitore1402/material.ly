import sys

from flask import Blueprint, render_template, request, session, flash, redirect, url_for

from forms import ArticleForm

sys.path.append('../')
from services.mysql_service import getConnection
from utils.common_utils import is_logged_in
sys.path.remove('../')

articles = Blueprint('articles', __name__,template_folder='templates')

# Articles
@articles.route('/articles')
def all_articles():
	conn = getConnection()
	cur = conn.cursor()
	result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.articles")

	articles = cur.fetchall()
	cur.close()
	if result > 0:
		return render_template('articles.html', articles = articles)
	else:
		msg = 'No Articles Found'
		return render_template('articles.html', msg = msg)

# Single Article
@articles.route('/article/<string:id>/')
def single_article(id):
	conn = getConnection()
	cur = conn.cursor()

	result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.articles WHERE id = %s", [id])

	article = cur.fetchone()
	cur.close()

	return render_template('article.html', article = article)

@articles.route('/add_article/', methods = ['GET', 'POST'])
@is_logged_in
def addArticle():
	form = ArticleForm(request.form)
	if request.method == 'POST' and form.validate():
		title = form.title.data
		body = form.body.data

		conn = getConnection()
		cur = conn.cursor()
		cur.execute("INSERT INTO rloveshhenko$mydbtest.articles(title,body,author) VALUES(%s, %s, %s)", (title,body,session['username']))
		conn.commit()
		cur.close()
		flash('Article Created', 'success')
		return redirect(url_for('dashboard_route.dashboard'))
	return render_template('add_article.html', form = form)

# Edit article
@articles.route('/edit_article/<string:id>', methods = ['GET', 'POST'])
@is_logged_in
def editArticle(id):
	conn = getConnection()
	cur = conn.cursor()
	result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.articles WHERE id = %s and author=%s", (id,session['username']))
	article = cur.fetchone()
	if (not article):
		flash('Permission denied', 'danger')
		return redirect(url_for('dashboard_route.dashboard'))
	# Get form
	form = ArticleForm(request.form)
	# Populate form fields
	form.title.data = article['title']
	form.body.data = article['body']

	if request.method == 'POST' and form.validate():
		title = request.form['title']
		body = request.form['body']
		# DB cursor
		conn = getConn()
		cur = conn.cursor()
		result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.articles WHERE id = %s and author=%s", (id,session['username']))
		article = cur.fetchone()
		if (not article):
			flash('Permission denied', 'danger')
			return redirect(url_for('dashboard_route.dashboard'))
		cur.execute("UPDATE rloveshhenko$mydbtest.articles SET title = %s, body = %s WHERE id = %s", (title, body, id))
		conn.commit()
		cur.close()
		flash('Article Updated', 'success')
		return redirect(url_for('dashboard_route.dashboard'))
	return render_template('edit_article.html', form = form)

# Delete article
@articles.route('/delete_article/<string:id>', methods = ['POST'])
@is_logged_in
def deleteArticle(id):
	# Delete from DB
	conn = getConnection()
	cur = conn.cursor()
	result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.articles WHERE id = %s and author=%s", (id,session['username']))
	article = cur.fetchone()
	if (not article):
		flash('Permission denied', 'danger')
		return redirect(url_for('dashboard_route.dashboard'))
	cur.execute("DELETE FROM rloveshhenko$mydbtest.articles WHERE id = %s", [id])
	conn.commit()
	cur.close()
	flash('Article Deleted', 'success')
	return redirect(url_for('dashboard_route.dashboard'))