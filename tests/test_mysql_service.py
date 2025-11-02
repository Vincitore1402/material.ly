import importlib

import pytest


MySQLService = importlib.import_module('services.mysql_service').MySQLService


def test_get_connection_requires_mysql_driver():
  service = MySQLService()

  with pytest.raises(ModuleNotFoundError):
    service.get_connection()


class _FakeCursorMissing:
  def execute(self, query, params=None):
    return 0

  def fetchone(self):
    return None

  def close(self):
    pass


class _FakeCursorArticle:
  def __init__(self):
    self.delete_called = False

  def execute(self, query, params=None):
    if 'SELECT' in query.upper():
      self._result = {'id': 1, 'author': params[1] if isinstance(params, tuple) and len(params) > 1 else 'author'}
      return 1
    if 'DELETE' in query.upper():
      self.delete_called = True
      return 1
    return 0

  def fetchone(self):
    return getattr(self, '_result', None)

  def close(self):
    pass


class _FakeConnection:
  def __init__(self, cursor):
    self._cursor = cursor
    self.committed = False

  def cursor(self):
    return self._cursor

  def commit(self):
    self.committed = True


def test_delete_article_by_id_returns_false_when_not_found(monkeypatch):
  monkeypatch.setattr(MySQLService, 'get_connection', staticmethod(lambda: _FakeConnection(_FakeCursorMissing())))
  service = MySQLService()

  assert service.delete_article_by_id(1, 'user') is False


def test_delete_article_by_id_removes_existing(monkeypatch):
  cursor = _FakeCursorArticle()
  connection = _FakeConnection(cursor)
  monkeypatch.setattr(MySQLService, 'get_connection', staticmethod(lambda: connection))
  service = MySQLService()

  assert service.delete_article_by_id(2, 'author') is True
  assert cursor.delete_called is True
  assert connection.committed is True


class _FakeCursorUsers:
  def __init__(self, user_exists=False, password='secret'):
    self.user_exists = user_exists
    self._user = {'password': password, 'username': 'user'} if user_exists else None

  def execute(self, query, params=None):
    if 'SELECT' in query.upper():
      return 1 if self.user_exists else 0
    if 'INSERT' in query.upper():
      self.user_exists = True
      return 1
    return 0

  def fetchone(self):
    return self._user

  def close(self):
    pass


def test_register_user_returns_false_for_existing(monkeypatch):
  connection = _FakeConnection(_FakeCursorUsers(user_exists=True))
  monkeypatch.setattr(MySQLService, 'get_connection', staticmethod(lambda: connection))
  service = MySQLService()

  user = type('User', (), {'name': 'Name', 'email': 'email', 'username': 'user', 'password': 'secret'})
  assert service.register_user(user) is False


def test_register_user_saves_new_user(monkeypatch):
  cursor = _FakeCursorUsers(user_exists=False)
  connection = _FakeConnection(cursor)
  monkeypatch.setattr(MySQLService, 'get_connection', staticmethod(lambda: connection))
  service = MySQLService()

  user = type('User', (), {'name': 'Name', 'email': 'email', 'username': 'user', 'password': 'secret'})
  assert service.register_user(user) is True
  assert connection.committed is True


def test_login_returns_user_when_password_matches(monkeypatch):
  cursor = _FakeCursorUsers(user_exists=True, password='secret')
  connection = _FakeConnection(cursor)
  monkeypatch.setattr(MySQLService, 'get_connection', staticmethod(lambda: connection))
  service = MySQLService()

  assert service.login('user', 'secret') == cursor._user


def test_login_returns_false_when_user_missing(monkeypatch):
  cursor = _FakeCursorUsers(user_exists=False)
  connection = _FakeConnection(cursor)
  monkeypatch.setattr(MySQLService, 'get_connection', staticmethod(lambda: connection))
  service = MySQLService()

  assert service.login('user', 'secret') is False
