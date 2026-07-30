ROLES = {
    "admin": ["read", "write", "delete", "manage_users", "manage_roles"],
    "manager": ["read", "write", "manage_users"],
    "editor": ["read", "write"],
    "viewer": ["read"],
}

def has_permission(user_role: str, required_permission: str) -> bool:
    if user_role not in ROLES:
        return False
    return required_permission in ROLES[user_role]

def require_permission(permission: str):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            user = getattr(request, "user", None)
            if not user or not has_permission(user.get("role", ""), permission):
                from flask import abort
                abort(403, f"Missing required permission: {permission}")
            return func(request, *args, **kwargs)
        return wrapper
    return decorator
