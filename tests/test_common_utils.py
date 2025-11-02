import importlib

from flask import _flashes, session


def _reload_common_utils():
  module = importlib.import_module('utils.common_utils')
  importlib.reload(module)
  return module


def test_is_logged_in_redirects_when_user_missing(monkeypatch):
  module = _reload_common_utils()

  session.clear()
  _flashes.clear()

  @module.is_logged_in
  def protected():
    return 'allowed'

  result = protected()

  assert result == ('redirect', '/auth.login')
  assert _flashes[-1] == ('Unauthorized, Please login', 'danger')


def test_is_logged_in_allows_logged_user(monkeypatch):
  module = _reload_common_utils()

  session.clear()
  _flashes.clear()
  session['logged_in'] = True

  @module.is_logged_in
  def protected():
    return 'allowed'

  assert protected() == 'allowed'


def test_write_and_load_data_round_trip(tmp_path):
  module = _reload_common_utils()

  data_dir = tmp_path / 'data'
  data_dir.mkdir()

  module.config.PROJECT_DIRECTORY = str(data_dir) + '/'
  payload = {'hello': 'world', 'count': 3}

  module.write_data_to_file(payload, 'test.json')
  loaded = module.load_data_from_file('test.json')

  assert loaded == payload


def test_write_csv_creates_expected_rows(tmp_path):
  module = _reload_common_utils()

  csv_file = tmp_path / 'out.csv'
  data = [
    {
      'id': 1,
      'composition': [{'average': value} for value in range(14)]
    }
  ]

  module.write_csv(str(csv_file), data)

  contents = csv_file.read_text().splitlines()

  assert contents[0].startswith('id,1,2,3')
  assert contents[1].startswith('1,0,1,2')
