import MySQLdb
import MySQLdb.cursors

from passlib.hash import sha256_crypt

from flask import flash, request
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

  def delete_material_by_id(self, id):
    # Delete from DB
    conn = self.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM rloveshhenko$mydbtest.main_info WHERE id = %s", [id])
    material = cur.fetchone()
    if not material:
      return False
    # cur.execute("DELETE FROM rloveshhenko$mydbtest.main_info WHERE id = %s", [id])
    cur.execute("DELETE FROM rloveshhenko$mydbtest.chemical_composition WHERE main_info_id = %s", [id])
    cur.execute("DELETE FROM rloveshhenko$mydbtest.critical_temperature WHERE main_info_id = %s", [id])
    cur.execute("DELETE FROM rloveshhenko$mydbtest.mechanical_properties WHERE main_info_id = %s", [id])
    cur.execute("DELETE FROM rloveshhenko$mydbtest.physical_properties WHERE main_info_id = %s", [id])
    cur.execute("DELETE FROM rloveshhenko$mydbtest.table6 WHERE main_info_id = %s", [id])
    cur.execute("DELETE FROM rloveshhenko$mydbtest.techno_properties WHERE main_info_id = %s", [id])
    cur.execute("DELETE FROM rloveshhenko$mydbtest.termo_mode WHERE main_info_id = %s", [id])
    conn.commit()
    cur.close()
    return True

  def addOtherTableMaterial(self, form):
    conn = self.getConnection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM rloveshhenko$mydbtest.main_info ORDER BY id DESC LIMIT 1")
    id = cur.fetchone()

    if request.form['btn'] == 'Add chemical composition':
      cur.execute(
        "INSERT INTO rloveshhenko$mydbtest.chemical_composition(main_info_id,atomic_Number,concetration,minimum,maximum,average) VALUES(%s, %s, %s, %s, %s, %s)",
        (id['id'], form.AtomicNumber.data, form.concentration.data, form.minimum.data, form.maximum.data,
         form.average.data))

      conn.commit()
      cur.close()
      flash('Table add', 'success')
      return

    if request.form['btn'] == 'Add critical temperatur':
      cur.execute(
        "INSERT INTO rloveshhenko$mydbtest.critical_temperature(main_info_id,critical_temperature) VALUES(%s, %s)",
        (id['id'], form.critical_temperatur.data))

      conn.commit()
      cur.close()
      flash('Table add', 'success')
      return

    if request.form['btn'] == 'Add mechanical properties':
      cur.execute(
        "INSERT INTO rloveshhenko$mydbtest.mechanical_properties(main_info_id,sortament,razmer,napr,sigma_b,sigma_t,delta_5,psi,KCU,termo_obrab) VALUES(%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)",
        (id['id'], form.sortament.data, form.razmer.data, form.napr.data, form.sigma_b.data, form.sigma_t.data,
         form.delta_5.data, form.psi.data, form.KCU.data, form.termo_obrab.data))

      conn.commit()
      cur.close()
      flash('Table add', 'success')
      return

    if request.form['btn'] == 'Add phisical properties':
      cur.execute(
        "INSERT INTO rloveshhenko$mydbtest.physical_properties(main_info_id,T,E,alpha,lambda,ro,C,R) VALUES(%s, %s,%s, %s,%s, %s,%s, %s)",
        (
          id['id'], form.T.data, form.E.data, form.alpha.data, form.LAMBDAA.data, form.ro.data, form.C.data,
          form.R.data))

      conn.commit()
      cur.close()
      flash('Table add', 'success')
      return

    if request.form['btn'] == 'Add table6':
      cur.execute(
        "INSERT INTO rloveshhenko$mydbtest.table6(main_info_id,property) VALUES(%s, %s)",
        (id['id'], form.property.data))

      conn.commit()
      cur.close()
      flash('Table add', 'success')
      return

    if request.form['btn'] == 'Add techno properties':
      cur.execute(
        "INSERT INTO rloveshhenko$mydbtest.techno_properties(main_info_id,property_name, property_value) VALUES(%s, %s, %s)",
        (id['id'], form.property_name.data, form.property_value.data))

      conn.commit()
      cur.close()
      flash('Table add', 'success')
      return

    if request.form['btn'] == 'Add termo mod':
      cur.execute(
        "INSERT INTO rloveshhenko$mydbtest.termo_mode(main_info_id,property) VALUES(%s, %s)",
        (id['id'], form.property.data))

      conn.commit()
      cur.close()
      flash('Table add', 'success')
      return

  def get_all_materials(self, page_number, materials_per_page):
    conn = self.get_connection()
    cur = conn.cursor()
    total = cur.execute("SELECT * FROM rloveshhenko$mydbtest.main_info")

    total_page = int(total / materials_per_page) + 1

    cur.execute("SELECT * FROM rloveshhenko$mydbtest.main_info limit %s,%s",
                ((page_number - 1) * materials_per_page, materials_per_page))
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
