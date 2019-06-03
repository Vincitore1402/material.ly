import MySQLdb
import MySQLdb.cursors
# TODO

from passlib.hash import sha256_crypt

from utils.common_utils import get_config

config = get_config()


class MySQLService:
  @staticmethod
  def get_connection():
    conn = MySQLdb.connect(host=config.DB_HOST, user=config.DB_USER, passwd=config.DB_PASSWORD, db=config.DB_NAME,
                           charset=config.DEFAULT_CHARSET, cursorclass=MySQLdb.cursors.DictCursor)
    return conn

  def get_all_articles(self):
    conn = self.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM rloveshhenko$mydbtest.articles")
    articles = cur.fetchall()
    cur.close()
    return articles

  def get_article_by_id(self, id):
    conn = self.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM rloveshhenko$mydbtest.articles WHERE id = %s", [id])
    article = cur.fetchone()
    cur.close()
    return article

  def get_articles_by_author(self, author):
    conn = self.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM rloveshhenko$mydbtest.articles WHERE author = %s", [author])
    articles = cur.fetchall()
    cur.close()
    return articles

  def get_article_by_id_and_author(self, id, author):
    conn = self.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM rloveshhenko$mydbtest.articles WHERE id = %s and author=%s",
                (id, author))
    article = cur.fetchone()
    cur.close()
    return article

  def delete_article_by_id(self, id, username):
    # Delete from DB
    conn = self.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM rloveshhenko$mydbtest.articles WHERE id = %s and author=%s",
                (id, username))
    article = cur.fetchone()

    if not article:
      return False
    cur.execute("DELETE FROM rloveshhenko$mydbtest.articles WHERE id = %s", [id])
    conn.commit()
    cur.close()
    return True

  def update_article_by_id(self, id, article):
    conn = self.get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE rloveshhenko$mydbtest.articles SET title = %s, body = %s WHERE id = %s",
                (article.title, article.body, id))
    conn.commit()
    cur.close()
    return article

  def add_article(self, article):
    conn = self.get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO rloveshhenko$mydbtest.articles(title,body,author) VALUES(%s, %s, %s)",
                (article.title, article.body, article.author))
    conn.commit()
    cur.close()
    return article

  def get_all_materials(self, numPage, materialsPerPage):
    conn = self.get_connection()
    cur = conn.cursor()
    total = cur.execute("SELECT * FROM rloveshhenko$mydbtest.main_info")

    total_page = int(total / materialsPerPage) + 1

    cur.execute("SELECT * FROM rloveshhenko$mydbtest.main_info limit %s,%s",
                ((numPage - 1) * materialsPerPage, materialsPerPage))
    materials = cur.fetchall()
    cur.close()
    return materials, total_page

  def register_user(self, user):
    conn = self.get_connection()
    cur = conn.cursor()

    if cur.execute("SELECT * FROM rloveshhenko$mydbtest.users WHERE username = %s", [user.username]) > 0:
      return False

    cur.execute("INSERT INTO rloveshhenko$mydbtest.users(name, email, username, password) VALUES(%s, %s, %s, %s)",
                (user.name, user.email, user.username, user.password))
    conn.commit()
    cur.close()

    return True

  def login(self, username, password_candidate):
    conn = self.get_connection()
    cur = conn.cursor()

    if not cur.execute("SELECT * FROM rloveshhenko$mydbtest.users WHERE username = %s", [username]) > 0:
      return False

    user = cur.fetchone()
    password = user['password']

    cur.close()

    return user if sha256_crypt.verify(password_candidate, password) else False

