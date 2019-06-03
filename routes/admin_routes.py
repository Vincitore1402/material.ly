import sys

from sqlalchemy.sql.functions import current_user

from forms.forms import MaterialFormMain, MaterialFormOther

from flask import Blueprint, render_template, sessions, redirect, url_for, flash, request, session

sys.path.append('../')
from services.mysql_service import MySQLService

sys.path.remove('../')

from utils.common_utils import getConfig
from utils.common_utils import is_logged_in

config = getConfig()

dbExample = MySQLService()

adminExample = Blueprint('adminExample', __name__,template_folder='templates')

def deleteMaterialAdmin(id):
    result = dbExample.deleteMaterialById(id)
    if (result == False):
        flash('Error: not deleted', 'danger')
        return redirect(url_for('admin.index'))
    flash('Material Deleted', 'success')
    return redirect(url_for('admin.index'))


def getForm():
    form = MaterialFormOther(request.form)
    return form