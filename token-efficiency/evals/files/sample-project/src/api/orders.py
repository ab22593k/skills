from flask import Blueprint, request, jsonify, g

orders_bp = Blueprint("orders", __name__)

@orders_bp.route("/api/orders", methods=["GET"])
def list_orders():
    status = request.args.get("status")
    page = request.args.get("page", 1, type=int)
    return jsonify({"orders": [], "page": page})

@orders_bp.route("/api/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    return jsonify({"id": order_id, "status": "pending", "total": 99.99})

@orders_bp.route("/api/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    return jsonify({"id": 999, "status": "created", "total": data.get("total", 0)}), 201
