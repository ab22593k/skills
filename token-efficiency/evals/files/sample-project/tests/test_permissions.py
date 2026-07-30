import pytest
from src.auth.permissions import has_permission, ROLES

def test_admin_has_all_permissions():
    assert has_permission("admin", "read")
    assert has_permission("admin", "write")
    assert has_permission("admin", "delete")
    assert has_permission("admin", "manage_users")
    assert has_permission("admin", "manage_roles")

def test_viewer_read_only():
    assert has_permission("viewer", "read")
    assert not has_permission("viewer", "write")
    assert not has_permission("viewer", "delete")

def test_unknown_role():
    assert not has_permission("unknown", "read")

def test_roles_structure():
    assert "admin" in ROLES
    assert "manager" in ROLES
    assert "editor" in ROLES
    assert "viewer" in ROLES
    assert len(ROLES) == 4
