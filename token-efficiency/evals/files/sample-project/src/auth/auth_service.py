import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional

SECRET_KEY = "dev-secret-key-not-for-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthService:
    def __init__(self, user_repo, token_store=None):
        self.user_repo = user_repo
        self.token_store = token_store

    def authenticate(self, username: str, password: str) -> Optional[dict]:
        user = self.user_repo.find_by_username(username)
        if not user or not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
            return None
        return {
            "user_id": user["id"],
            "username": user["username"],
            "role": user["role"],
        }

    def create_access_token(self, user_data: dict) -> str:
        payload = {
            "sub": str(user_data["user_id"]),
            "username": user_data["username"],
            "role": user_data["role"],
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            "iat": datetime.utcnow(),
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def verify_token(self, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def refresh_token(self, token: str) -> Optional[str]:
        payload = self.verify_token(token)
        if not payload:
            return None
        return self.create_access_token({
            "user_id": payload["sub"],
            "username": payload["username"],
            "role": payload["role"],
        })
