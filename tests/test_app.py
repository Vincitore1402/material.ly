import os
import sys

import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
  sys.path.insert(0, ROOT_DIR)

pytest.importorskip('flask')
pytest.importorskip('flask_sqlalchemy')

from app import create_app


def test_create_app_uses_override_database_uri():
  override_uri = 'sqlite:///:memory:'
  secret_key = 'testing-key'
  app = create_app({'SQLALCHEMY_DATABASE_URI': override_uri, 'SECRET_KEY': secret_key})

  assert app.config['SQLALCHEMY_DATABASE_URI'] == override_uri
  assert app.secret_key == secret_key


def test_blueprints_are_registered():
  app = create_app({'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})

  registered = set(app.blueprints.keys())
  expected = {
    'index_page',
    'about_page',
    'articles',
    'materials',
    'auth',
    'visualization',
    'dashboard_route',
    'searches',
    'adminExample',
    'api'
  }

  assert expected.issubset(registered)
