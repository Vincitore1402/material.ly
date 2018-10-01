import MySQLdb
import MySQLdb.cursors
import sys

from utils.common_utils import getConfig

config = getConfig()

class MySQLService():
	def getConnection(self):
		conn = MySQLdb.connect(host=config.DB_HOST, user=config.DB_USER, passwd=config.DB_PASSWORD, db=config.DB_NAME,charset=config.DEFAULT_CHARSET,cursorclass=MySQLdb.cursors.DictCursor)
		return conn

	def getAllArticles(self):
		conn = self.getConnection()
		cur = conn.cursor()
		result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.articles")
		articles = cur.fetchall()
		cur.close()
		return articles

	def getArticleById(self, id):
		conn = self.getConnection()
		cur = conn.cursor()

		result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.articles WHERE id = %s", [id])

		article = cur.fetchone()
		cur.close()
		return article

	def getArticleByAuthor(self, author):
		conn = self.getConnection()
		cur = conn.cursor()
		username = session['username']
		result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.articles WHERE author = %s", [author])
		articles = cur.fetchall()
		cur.close()
		return articles

	def getArticleByIdAndAuthor(self, id, author):
		conn = self.getConnection()
		cur = conn.cursor()

		result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.articles WHERE id = %s and author=%s",
							 (id, author))

		article = cur.fetchone()
		cur.close()
		return article

	def deleteArticleById(self, id, username):
		# Delete from DB
		conn = self.getConnection()
		cur = conn.cursor()
		result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.articles WHERE id = %s and author=%s",
							 (id, username))
		article = cur.fetchone()
		if (not article):
			return False
		cur.execute("DELETE FROM rloveshhenko$mydbtest.articles WHERE id = %s", [id])
		conn.commit()
		cur.close()
		return True

	def updateArticleById(self, id, article):
		conn = self.getConnection()
		cur = conn.cursor()
		cur.execute("UPDATE rloveshhenko$mydbtest.articles SET title = %s, body = %s WHERE id = %s", (article.title, article.body, id))
		conn.commit()
		cur.close()
		return article


	def addArticle(self, article):
		conn = self.getConnection()
		cur = conn.cursor()
		cur.execute("INSERT INTO rloveshhenko$mydbtest.articles(title,body,author) VALUES(%s, %s, %s)",
					(article.title, article.body, article.author))
		conn.commit()
		cur.close()
		return article

	def getAllMaterials(self, numPage, materialsPerPage):
		conn = self.getConnection()
		cur = conn.cursor()
		total = cur.execute("SELECT * FROM rloveshhenko$mydbtest.main_info")
		# print (total)
		total_page = (int)(total / materialsPerPage) + 1
		# print (total_page)
		result = cur.execute("SELECT * FROM rloveshhenko$mydbtest.main_info limit %s,%s",
							 ((numPage - 1) * materialsPerPage, materialsPerPage))
		materials = cur.fetchall()
		cur.close()
		return materials, total_page