import sys
import types


def _install_flask_stub():
  if 'flask' in sys.modules:
    return

  flask = types.ModuleType('flask')

  _flashes = []

  class _Logger:
    def __init__(self):
      self.messages = []

    def info(self, message):
      self.messages.append(('info', message))

    def warning(self, message):
      self.messages.append(('warning', message))

    def error(self, message):
      self.messages.append(('error', message))

  class _CurrentApp:
    def __init__(self):
      self.logger = _Logger()

  class Blueprint:
    def __init__(self, name, import_name, template_folder=None):
      self.name = name
      self.import_name = import_name
      self.template_folder = template_folder
      self.routes = {}

    def route(self, rule, **options):
      def decorator(func):
        self.routes.setdefault(rule, []).append((func, options))
        return func

      return decorator

  class Flask:
    def __init__(self, import_name):
      self.import_name = import_name
      self.secret_key = None
      self.config = {}
      self.blueprints = {}
      self.error_handlers = {}

    def register_blueprint(self, blueprint):
      self.blueprints[blueprint.name] = blueprint

    def register_error_handler(self, code, handler):
      self.error_handlers[code] = handler

    def run(self, **_kwargs):
      return True

  class _Request:
    def __init__(self):
      self.method = 'GET'
      self.form = {}

  def render_template(template_name, **context):
    return template_name, context

  def flash(message, category):
    _flashes.append((message, category))

  def redirect(location):
    return 'redirect', location

  def url_for(endpoint, **_values):
    return f'/{endpoint}'

  def abort(code):
    raise RuntimeError(f'aborted {code}')

  flask.Blueprint = Blueprint
  flask.Flask = Flask
  flask.render_template = render_template
  flask.flash = flash
  flask.redirect = redirect
  flask.url_for = url_for
  flask.abort = abort
  flask.session = {}
  flask.request = _Request()
  flask.current_app = _CurrentApp()
  flask.sessions = types.SimpleNamespace(Session=dict)
  flask._flashes = _flashes

  sys.modules['flask'] = flask


def _install_flask_admin_stub():
  if 'flask_admin' in sys.modules:
    return

  flask_admin = types.ModuleType('flask_admin')

  def expose(_route='/', **_options):
    def decorator(func):
      return func

    return decorator

  class AdminIndexView:
    def __init__(self):
      pass

    def render(self, template, **context):
      return template, context

    def is_accessible(self):
      return True

    def __call__(self, *args, **kwargs):
      return self

  class Admin:
    def __init__(self, app, name, url=None, index_view=None):
      self.app = app
      self.name = name
      self.url = url
      self.index_view = index_view
      self.views = []

    def add_view(self, view):
      self.views.append(view)

  flask_admin.expose = expose
  flask_admin.Admin = Admin
  flask_admin.AdminIndexView = AdminIndexView

  sqla_module = types.ModuleType('flask_admin.contrib.sqla')

  class ModelView:
    def __init__(self, model, session, **kwargs):
      self.model = model
      self.session = session
      self.kwargs = kwargs

    def render(self, template, **context):
      return template, context

    def index_view(self):
      return 'index'

    def on_model_delete(self, _model):
      return None

  sqla_module.ModelView = ModelView

  contrib_module = types.ModuleType('flask_admin.contrib')
  contrib_module.sqla = sqla_module

  sys.modules['flask_admin'] = flask_admin
  sys.modules['flask_admin.contrib'] = contrib_module
  sys.modules['flask_admin.contrib.sqla'] = sqla_module


def _install_sqlalchemy_stub():
  if 'flask_sqlalchemy' not in sys.modules:
    flask_sqlalchemy = types.ModuleType('flask_sqlalchemy')

    class _DummyQuery:
      def filter(self, *_args, **_kwargs):
        return self

      def select_from(self, *_args, **_kwargs):
        return self

      def __iter__(self):
        return iter(())

    class _DummySession:
      def query(self, *_args, **_kwargs):
        return _DummyQuery()

    class _Column:
      def __init__(self, *_args, **_kwargs):
        pass

    class _Type:
      def __call__(self, *args, **kwargs):
        return {'args': args, 'kwargs': kwargs}

    class SQLAlchemy:
      def __init__(self):
        self.Model = type('Model', (), {})
        self.Column = _Column
        self.Integer = _Type()
        self.String = _Type()
        self.DateTime = _Type()
        self.session = _DummySession()

      def init_app(self, app):
        self.app = app

    flask_sqlalchemy.SQLAlchemy = SQLAlchemy

    sys.modules['flask_sqlalchemy'] = flask_sqlalchemy

  if 'sqlalchemy' not in sys.modules:
    sqlalchemy = types.ModuleType('sqlalchemy')
    sqlalchemy.func = types.SimpleNamespace(count=lambda *_args, **_kwargs: None)
    sys.modules['sqlalchemy'] = sqlalchemy

  sql_functions = types.ModuleType('sqlalchemy.sql.functions')
  sql_functions.current_user = object()
  sys.modules['sqlalchemy.sql.functions'] = sql_functions


def _install_passlib_stub():
  if 'passlib.hash' in sys.modules:
    return

  passlib = types.ModuleType('passlib')
  hash_module = types.ModuleType('passlib.hash')

  class _SHA256Crypt:
    @staticmethod
    def verify(candidate, hashed):
      return candidate == hashed

    @staticmethod
    def hash(value):
      return value

  hash_module.sha256_crypt = _SHA256Crypt
  passlib.hash = hash_module

  sys.modules['passlib'] = passlib
  sys.modules['passlib.hash'] = hash_module


def _install_pydash_stub():
  if 'pydash' in sys.modules:
    return

  pydash = types.ModuleType('pydash')

  def map_(iterable, function):
    return [function(item) for item in iterable]

  def filter_(iterable, predicate):
    return [item for item in iterable if predicate(item)]

  def reduce_(iterable, function, initial):
    result = initial
    for item in iterable:
      result = function(result, item)
    return result

  def get(obj, key, default=None):
    parts = key.split('.') if isinstance(key, str) else [key]
    value = obj
    for part in parts:
      if isinstance(value, dict):
        value = value.get(part, default)
      else:
        return default
    return value

  pydash.map_ = map_
  pydash.filter_ = filter_
  pydash.reduce_ = reduce_
  pydash.get = get

  sys.modules['pydash'] = pydash


def _install_numpy_stub():
  if 'numpy' in sys.modules:
    return

  numpy = types.ModuleType('numpy')

  class _Array(list):
    def astype(self, _dtype):
      return _Array(float(x) for x in self)

    def tolist(self):
      return list(self)

  def array(values):
    if isinstance(values, _Array):
      return values
    if isinstance(values, (list, tuple)):
      return _Array(values)
    return _Array(list(values))

  numpy.array = array

  sys.modules['numpy'] = numpy


def _install_pygal_stub():
  if 'pygal' in sys.modules:
    return

  pygal = types.ModuleType('pygal')

  class XY:
    def __init__(self, stroke=False):
      self.stroke = stroke
      self.title = ''
      self.series = []

    def add(self, key, value):
      self.series.append((key, value))

    def render_data_uri(self):
      return f'data:series={len(self.series)};title={self.title}'

  pygal.XY = XY

  sys.modules['pygal'] = pygal


def _install_sckit_stub():
  module_name = 'services.sckit_learn'
  if module_name in sys.modules:
    return

  stub = types.ModuleType(module_name)

  def start_manifold_learning(input_data):
    ids = input_data.get('ids', [])
    return {
      'Isomap': {'x': list(range(len(ids))), 'y': list(range(len(ids))), 'ids': ids, 'matInfo': input_data.get('matInfo', [])}
    }

  def start_regression_learning(_input):
    return None

  stub.start_manifold_learning = start_manifold_learning
  stub.start_regression_learning = start_regression_learning

  sys.modules[module_name] = stub


def _install_wtforms_stub():
  if 'wtforms' in sys.modules:
    return

  wtforms = types.ModuleType('wtforms')

  class _Field:
    def __init__(self, label='', validators=None):
      self.label = label
      self.validators = validators or []
      self.data = None

    def clone(self):
      return _Field(self.label, list(self.validators))

  class _FormMeta(type):
    def __new__(mcs, name, bases, attrs):
      fields = {k: v for k, v in attrs.items() if isinstance(v, _Field)}
      for key in fields:
        attrs.pop(key)
      cls = super().__new__(mcs, name, bases, attrs)
      cls._declared_fields = fields
      return cls

  class Form(metaclass=_FormMeta):
    def __init__(self, formdata=None):
      self._fields = {}
      for name, field in self._declared_fields.items():
        cloned = field.clone()
        self._fields[name] = cloned
        if formdata and name in formdata:
          cloned.data = formdata[name]
      self.formdata = formdata or {}

    def validate(self):
      return True

    def __getattr__(self, item):
      if item in self._fields:
        return self._fields[item]
      raise AttributeError(item)

  class StringField(_Field):
    pass

  class TextAreaField(_Field):
    pass

  class PasswordField(_Field):
    pass

  class Length:
    def __init__(self, min=None, max=None):
      self.min = min
      self.max = max

  class DataRequired:
    def __call__(self, *_args, **_kwargs):
      return True

  class EqualTo:
    def __init__(self, fieldname, message=None):
      self.fieldname = fieldname
      self.message = message

  validators = types.SimpleNamespace(Length=Length, DataRequired=DataRequired, EqualTo=EqualTo)

  wtforms.Form = Form
  wtforms.StringField = StringField
  wtforms.TextAreaField = TextAreaField
  wtforms.PasswordField = PasswordField
  wtforms.validators = validators

  sys.modules['wtforms'] = wtforms


def _install_jinja_stub():
  if 'jinja2' in sys.modules:
    return

  jinja = types.ModuleType('jinja2')

  class TemplateNotFound(Exception):
    pass

  jinja.TemplateNotFound = TemplateNotFound

  sys.modules['jinja2'] = jinja


def pytest_configure(config):
  _install_flask_stub()
  _install_flask_admin_stub()
  _install_sqlalchemy_stub()
  _install_passlib_stub()
  _install_pydash_stub()
  _install_numpy_stub()
  _install_pygal_stub()
  _install_sckit_stub()
  _install_wtforms_stub()
  _install_jinja_stub()
