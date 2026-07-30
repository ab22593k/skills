from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: int
    username: str
    email: str
    password_hash: str
    role: str
    created_at: datetime
    is_active: bool = True

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat(),
            "is_active": self.is_active,
        }

    def has_permission(self, permission):
        from src.auth.permissions import has_permission
        return has_permission(self.role, permission)
