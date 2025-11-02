import hashlib
import os
import sys
import types
from types import SimpleNamespace
from unittest.mock import MagicMock

# Ensure project root is importable
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# Provide a lightweight stub for the flask package so modules can be imported
if "flask" not in sys.modules:
    flask_stub = types.ModuleType("flask")

    class _Session(dict):
        pass

    session_storage = _Session()

    def flash(message, category):
        session_storage.setdefault("_flashes", []).append((category, message))

    def redirect(location):
        return SimpleNamespace(location=location)

    def url_for(endpoint):
        return f"/{endpoint.replace('.', '/')}"

    flask_stub.flash = flash
    flask_stub.redirect = redirect
    flask_stub.url_for = url_for
    flask_stub.session = session_storage
    flask_stub.request = SimpleNamespace(form={})
    flask_stub.Blueprint = SimpleNamespace
    flask_stub.Flask = SimpleNamespace

    sys.modules["flask"] = flask_stub


# Provide a deterministic implementation of passlib.sha256_crypt for hashing tests
if "passlib.hash" not in sys.modules:
    passlib_hash = types.ModuleType("passlib.hash")

    class _Sha256Crypt:
        @staticmethod
        def hash(value):
            return hashlib.sha256(value.encode("utf-8")).hexdigest()

        @staticmethod
        def verify(candidate, hashed):
            return _Sha256Crypt.hash(candidate) == hashed

    passlib_hash.sha256_crypt = _Sha256Crypt
    sys.modules["passlib.hash"] = passlib_hash


# Stub the MySQLdb module so imports succeed during testing
if "MySQLdb" not in sys.modules:
    mysql_module = types.ModuleType("MySQLdb")
    mysql_module.connect = MagicMock()

    cursors_module = types.ModuleType("MySQLdb.cursors")
    cursors_module.DictCursor = object

    mysql_module.cursors = cursors_module

    sys.modules["MySQLdb"] = mysql_module
    sys.modules["MySQLdb.cursors"] = cursors_module
