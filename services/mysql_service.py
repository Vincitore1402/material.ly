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