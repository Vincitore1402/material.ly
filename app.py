import MySQLdb
from flask import Flask
from flask_admin import Admin, expose, AdminIndexView
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import func
from datetime import datetime
from routes.admin_routes import *

from routes.static_pages import index_page, about_page
from routes.articles_routes import articles
from routes.materials_routes import materials
from routes.auth_routes import auth
from routes.visualizations_routes import visualization
from routes.dashboard import dashboard_route
from routes.search_routes import searches
from routes.admin_routes import adminExample
from routes.api_routes import api
from utils.common_utils import get_config

config = get_config()

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s' % (
config.DB_USER, config.DB_PASSWORD, config.DB_HOST, config.DB_NAME)
db = SQLAlchemy(app)

app.register_blueprint(index_page)
app.register_blueprint(about_page)
app.register_blueprint(articles)
app.register_blueprint(materials)
app.register_blueprint(auth)
app.register_blueprint(visualization)
app.register_blueprint(dashboard_route)
app.register_blueprint(searches)
app.register_blueprint(adminExample)
app.register_blueprint(api)


@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404


# Models
class Material(db.Model):
  __tablename__ = 'main_info'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), unique=True)
  marka = db.Column(db.String(30))
  classification = db.Column(db.String(128))
  dopolnenie = db.Column(db.String(128))
  primenenie = db.Column(db.String(128))


class User(db.Model):
  __tablename__ = 'users'
  can_delete = False

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), unique=True)
  email = db.Column(db.String(128))
  username = db.Column(db.String(30))
  register_date = db.Column(db.DateTime, default=datetime.now())


class ChemicalComposition(db.Model):
  __tablename__ = 'chemical_composition'

  id = db.Column(db.Integer, primary_key=True)
  main_info_id = db.Column(db.String(20))
  atomic_Number = db.Column(db.String(30))
  concetration = db.Column(db.String(30))
  minimum = db.Column(db.String(30))
  maximum = db.Column(db.String(30))
  average = db.Column(db.String(30))


class CriticalTemperature(db.Model):
  __tablename__ = 'critical_temperature'

  id = db.Column(db.Integer, primary_key=True)
  main_info_id = db.Column(db.String(20))
  critical_temperature = db.Column(db.String(500))


class MechanicalProperties(db.Model):
  __tablename__ = 'mechanical_properties'

  id = db.Column(db.Integer, primary_key=True)
  main_info_id = db.Column(db.String(20))
  sortament = db.Column(db.String(200))
  razmer = db.Column(db.String(20))
  napr = db.Column(db.String(20))
  sigma_b = db.Column(db.String(20))
  sigma_t = db.Column(db.String(20))
  delta_5 = db.Column(db.String(20))
  psi = db.Column(db.String(20))
  KCU = db.Column(db.String(20))
  termo_obrab = db.Column(db.String(100))


class PhysicalProperties(db.Model):
  __tablename__ = 'physical_properties'

  id = db.Column(db.Integer, primary_key=True)
  main_info_id = db.Column(db.String(20))
  T = db.Column(db.String(20))
  E = db.Column(db.String(20))
  alpha = db.Column(db.String(20))
  LAMBDA = db.Column(db.String(20))
  ro = db.Column(db.String(20))
  C = db.Column(db.String(20))
  R = db.Column(db.String(20))


class Table6(db.Model):
  __tablename__ = 'table6'

  id = db.Column(db.Integer, primary_key=True)
  main_info_id = db.Column(db.String(20))
  property = db.Column(db.String(500))


class TechnoProperties(db.Model):
  __tablename__ = 'techno_properties'

  id = db.Column(db.Integer, primary_key=True)
  main_info_id = db.Column(db.String(20))
  property_name = db.Column(db.String(200))
  property_value = db.Column(db.String(200))


class TermoMode(db.Model):
  __tablename__ = 'termo_mode'

  id = db.Column(db.Integer, primary_key=True)
  main_info_id = db.Column(db.String(20))
  property = db.Column(db.String(500))


class MyModelViewUser(ModelView):
  can_create = False


class MyModelViewMaterial(ModelView):
  column_searchable_list = ['name']

  def on_model_delete(self, model):
    delete_material_admin(model.id)
    return super(MyModelViewMaterial, self).on_model_delete(model)

  list_template = "admin_materials_list.html"
  create_template = 'admin_create_material.html'

  @expose("/", methods=['GET', 'POST'])
  def edit_other_table(self):

    if request.method == 'POST':

      if request.form['btn'] == 'Chemical':
        MCC.id = request.form['MaterialId']
        return redirect(url_for('ChemicalComposition.index_view'))
      if request.form['btn'] == 'Temperature':
        MCT.id = request.form['MaterialId']
        return redirect(url_for('CriticalTemperature.index_view'))
      if request.form['btn'] == 'Mechanical':
        MMP.id = request.form['MaterialId']
        return redirect(url_for('MechanicalProperties.index_view'))
      if request.form['btn'] == 'Physical':
        MPP.id = request.form['MaterialId']
        return redirect(url_for('PhysicalProperties.index_view'))
      if request.form['btn'] == 'Table6':
        MT6.id = request.form['MaterialId']
        return redirect(url_for('Table6.index_view'))
      if request.form['btn'] == 'TechnoProperties':
        MTP.id = request.form['MaterialId']
        return redirect(url_for('TechnoProperties.index_view'))
      if request.form['btn'] == 'TermoMode':
        MTM.id = request.form['MaterialId']
        return redirect(url_for('TermoMode.index_view'))

    return self.index_view()

  @expose('addMaterial', methods=['GET', 'POST'])
  def add_material(self):
    form = MaterialFormMain(request.form)
    if request.method == 'POST' and form.validate():
      classification = form.classification.data
      marka = form.marka.data
      primenenie = form.primenenie.data
      dopolnenie = form.dopolnenie.data

      # Create cursor
      conn = dbExample.getConnection()
      cur = conn.cursor()

      cur.execute(
        "INSERT INTO rloveshhenko$mydbtest.main_info(name, marka, classification, dopolnenie, primenenie) VALUES(%s, %s, %s, %s, %s)",
        ("Характеристика материала " + marka, marka, classification, dopolnenie, primenenie))
      # Commit to DB
      conn.commit()
      # Close the connection
      cur.close()

      flash('Table add', 'success')
      return self.render("add_material_other_table.html", form=get_form())
    return self.render("add_material.html", form=form)

  @expose('addMaterialOtherTable', methods=['GET', 'POST'])
  def add_material_other_table(self):
    try:
      form = MaterialFormOther(request.form)
      if request.method == 'POST' and form.validate():
        if request.form['btn'] == 'Done':
          return redirect(url_for('mat.editOtherTable'))
        else:
          dbExample.addOtherTableMaterial(form)
          return self.render("add_material_other_table.html", form=form)
      return self.render('add_material_other_table.html', form=get_form())
    except MySQLdb._exceptions.OperationalError:
      flash('Заполните все поля', 'danger')
      return self.render("add_material_other_table.html", form=get_form())


class CommonModel(ModelView):
  id = 0

  # readonly_fields = ('id',)

  def get_query(self):
    if self.id != 0:
      copy_id = self.id
      return self.session.query(self.model).filter(self.model.main_info_id == copy_id)
    else:
      return self.session.query(self.model)

  def get_count_query(self):
    if self.id != 0:
      copy_id = self.id
      self.id = 0
      return self.session.query(func.count('*')).filter(self.model.main_info_id == copy_id)
    else:
      return self.session.query(func.count('*')).select_from(self.model)


class ModelChemicalComposition(CommonModel):
  form_columns = ['main_info_id', 'atomic_Number', 'concetration', 'minimum', 'maximum', 'average']


class ModelCriticalTemperature(CommonModel):
  form_columns = ['main_info_id', 'critical_temperature']


class ModelMechanicalProperties(CommonModel):
  form_columns = ['main_info_id', 'sortament', 'razmer', 'napr', 'sigma_b', 'sigma_t', 'delta_5', 'psi', 'KCU',
                  'termo_obrab']


class ModelPhysicalProperties(CommonModel):
  form_columns = ['main_info_id', 'T', 'E', 'alpha', 'LAMBDA', 'ro', 'C', 'R']


class ModelTable6(CommonModel):
  form_columns = ['main_info_id', 'property']


class ModelTechnoProperties(CommonModel):
  form_columns = ['main_info_id', 'property_name', 'property_value']


class ModelTermoMode(CommonModel):
  form_columns = ['main_info_id', 'property']


class MyModelIndexView(AdminIndexView):
  @expose('/')
  def index(self):
    return self.render('admin_home.html')

  def is_accessible(self):
    try:
      if session['username'] == 'admin':
        return True
    except Exception:
      return False


MCC = ModelChemicalComposition(ChemicalComposition, db.session, category='OtherTable', endpoint='ChemicalComposition')
MCT = ModelCriticalTemperature(CriticalTemperature, db.session, category='OtherTable', endpoint="CriticalTemperature")
MMP = ModelMechanicalProperties(MechanicalProperties, db.session, category='OtherTable',
                                endpoint='MechanicalProperties')
MPP = ModelPhysicalProperties(PhysicalProperties, db.session, category='OtherTable', endpoint='PhysicalProperties')
MT6 = ModelTable6(Table6, db.session, category='OtherTable', endpoint="Table6")
MTP = ModelTechnoProperties(TechnoProperties, db.session, category='OtherTable', endpoint='TechnoProperties')
MTM = ModelTermoMode(TermoMode, db.session, category='OtherTable', endpoint='TermoMode')

admin = Admin(app, "Admin", url='/AdminPanel', index_view=MyModelIndexView())

admin.add_view(MyModelViewMaterial(Material, db.session, endpoint='mat'))
admin.add_view(MCC)
admin.add_view(MCT)
admin.add_view(MMP)
admin.add_view(MPP)
admin.add_view(MT6)
admin.add_view(MTP)
admin.add_view(MTM)
admin.add_view(MyModelViewUser(User, db.session))

if __name__ == '__main__':
  app.run(debug=True)
