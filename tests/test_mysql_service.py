from types import SimpleNamespace
from unittest.mock import MagicMock, patch
from unittest.mock import call

import pytest
from passlib.hash import sha256_crypt

from services.mysql_service import MySQLService


@pytest.fixture
def service():
    return MySQLService()


@pytest.fixture
def user():
    return SimpleNamespace(name="Bob", email="bob@example.com", username="bobby", password="hashed")


def _make_connection(cursor):
    conn = MagicMock()
    conn.cursor.return_value = cursor
    return conn


def test_register_user_rejects_existing_username(service, user):
    cursor = MagicMock()
    cursor.execute.return_value = 1
    conn = _make_connection(cursor)

    with patch.object(MySQLService, "get_connection", return_value=conn):
        assert service.register_user(user) is False

    conn.commit.assert_not_called()


def test_register_user_inserts_new_user(service, user):
    cursor = MagicMock()
    cursor.execute.side_effect = [0, None]
    conn = _make_connection(cursor)

    with patch.object(MySQLService, "get_connection", return_value=conn):
        assert service.register_user(user) is True

    assert conn.commit.called
    cursor.close.assert_called_once()

    select_call, insert_call = cursor.execute.call_args_list
    assert "SELECT * FROM rloveshhenko$mydbtest.users WHERE username = %s" in select_call[0][0]
    assert "INSERT INTO rloveshhenko$mydbtest.users" in insert_call[0][0]


def test_login_returns_user_on_success(service):
    cursor = MagicMock()
    cursor.execute.return_value = 1
    password = sha256_crypt.hash("secret")
    expected_user = {"password": password, "id": 1, "username": "bobby"}
    cursor.fetchone.return_value = expected_user
    conn = _make_connection(cursor)

    with patch.object(MySQLService, "get_connection", return_value=conn):
        result = service.login("bobby", "secret")

    assert result == expected_user
    cursor.close.assert_called_once()


def test_login_returns_false_when_password_invalid(service):
    cursor = MagicMock()
    cursor.execute.return_value = 1
    cursor.fetchone.return_value = {"password": sha256_crypt.hash("secret"), "id": 1}
    conn = _make_connection(cursor)

    with patch.object(MySQLService, "get_connection", return_value=conn):
        assert service.login("bobby", "wrong") is False


def test_login_returns_false_when_user_missing(service):
    cursor = MagicMock()
    cursor.execute.return_value = 0
    conn = _make_connection(cursor)

    with patch.object(MySQLService, "get_connection", return_value=conn):
        assert service.login("bobby", "secret") is False


def test_delete_material_by_id_returns_false_when_missing(service):
    cursor = MagicMock()
    cursor.fetchone.return_value = None
    conn = _make_connection(cursor)

    with patch.object(MySQLService, "get_connection", return_value=conn):
        assert service.delete_material_by_id(5) is False

    conn.commit.assert_not_called()


def test_delete_material_by_id_executes_cascading_deletes(service):
    cursor = MagicMock()
    cursor.fetchone.return_value = {"id": 5}
    conn = _make_connection(cursor)

    with patch.object(MySQLService, "get_connection", return_value=conn):
        assert service.delete_material_by_id(5) is True

    assert conn.commit.called
    executed_queries = [call.args[0] for call in cursor.execute.call_args_list]
    # First call is the SELECT, following calls should be DELETE statements for each table
    assert executed_queries[0].startswith("SELECT * FROM rloveshhenko$mydbtest.main_info")
    delete_statements = executed_queries[1:]
    assert any("chemical_composition" in statement for statement in delete_statements)
    assert any("critical_temperature" in statement for statement in delete_statements)
    assert any("mechanical_properties" in statement for statement in delete_statements)
    assert any("physical_properties" in statement for statement in delete_statements)
    assert any("table6" in statement for statement in delete_statements)
    assert any("techno_properties" in statement for statement in delete_statements)
    assert any("termo_mode" in statement for statement in delete_statements)
