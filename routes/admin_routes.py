from sqlalchemy.sql.functions import current_user

from forms.forms import MaterialFormMain, MaterialFormOther

from flask import Blueprint, render_template, sessions, redirect, url_for, flash, request, session

from services.mysql_service import MySQLService

from utils.common_utils import get_config

config = get_config()

dbExample = MySQLService()

adminExample = Blueprint('adminExample', __name__, template_folder='templates')


def delete_material_admin(id):
  result = dbExample.delete_material_by_id(id)
  if not result:
    flash('Error: not deleted', 'danger')
    return redirect(url_for('admin.index'))
  flash('Material Deleted', 'success')
  return redirect(url_for('admin.index'))


def get_form():
  form = MaterialFormOther(request.form)
  return form
