import pytest
from src.auth.auth_service import AuthService

class MockUserRepo:
    def __init__(self):
        self.users = {
            "alice": {"id": 1, "username": "alice", "password_hash": "", "role": "admin"},
            "bob": {"id": 2, "username": "bob", "password_hash": "", "role": "viewer"},
        }

    def find_by_username(self, username):
        return self.users.get(username)

def test_authenticate_valid_user():
    repo = MockUserRepo()
    service = AuthService(repo)
    result = service.authenticate("alice", "wrong-password")
    assert result is None

def test_verify_expired_token():
    repo = MockUserRepo()
    service = AuthService(repo)
    result = service.verify_token("invalid-token")
    assert result is None

def test_create_and_verify_token():
    repo = MockUserRepo()
    service = AuthService(repo)
    user_data = {"user_id": 1, "username": "alice", "role": "admin"}
    token = service.create_access_token(user_data)
    assert token is not None
    payload = service.verify_token(token)
    assert payload is not None
    assert payload["username"] == "alice"
