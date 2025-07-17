import pytest
import pytest

from auth_rbac import AuthManager, Role


def test_user_creation_and_verification(temp_auth_db):
    am = AuthManager(db_path=temp_auth_db)
    assert am.add_user("bob", "secret", Role.OPERATOR)
    assert am.verify_user("bob", "secret") == Role.OPERATOR
    assert am.verify_user("bob", "bad") is None
    cur = am.conn.cursor()
    cur.execute("SELECT password_hash FROM users WHERE username=?", ("bob",))
    stored = cur.fetchone()[0]
    assert stored != "secret"


def test_role_permissions():
    am = AuthManager(db_path=":memory:")
    assert am.is_allowed(Role.ADMIN, Role.OPERATOR)
    assert not am.is_allowed(Role.OPERATOR, Role.ADMIN)
