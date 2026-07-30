from flask import Blueprint, request, jsonify

products_bp = Blueprint("products", __name__)

@products_bp.route("/api/products", methods=["GET"])
def list_products():
    category = request.args.get("category")
    return jsonify({"products": [], "category": category})

@products_bp.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    return jsonify({"id": product_id, "name": "Example Product", "price": 29.99})

@products_bp.route("/api/products", methods=["POST"])
def create_product():
    data = request.get_json()
    return jsonify({"id": 1, "name": data.get("name")}), 201
