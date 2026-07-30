from flask import Blueprint, request, jsonify, g
from src.auth.auth_service import AuthService
from src.auth.permissions import has_permission

users_bp = Blueprint("users", __name__)

@users_bp.route("/api/users", methods=["GET"])
def list_users():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    # ... users listing logic
    return jsonify({"users": [], "page": page, "per_page": per_page})

@users_bp.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    # ... get user logic
    return jsonify({"id": user_id, "username": "example"})

@users_bp.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    # ... create user logic
    return jsonify({"id": 1, "username": data.get("username")}), 201
