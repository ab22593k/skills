from flask import request, jsonify, g
from functools import wraps
from src.auth.auth_service import AuthService

def auth_middleware(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid authorization header"}), 401

        token = auth_header[7:]
        auth_service = AuthService(None)
        payload = auth_service.verify_token(token)

        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401

        g.user = {
            "user_id": int(payload["sub"]),
            "username": payload["username"],
            "role": payload["role"],
        }
        return f(*args, **kwargs)
    return decorated
