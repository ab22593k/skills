import pytest
from src.models.user import User
from src.models.order import Order, OrderItem
from datetime import datetime

def test_user_to_dict():
    user = User(id=1, username="alice", email="alice@example.com", password_hash="hash", role="admin", created_at=datetime(2026, 1, 1))
    d = user.to_dict()
    assert d["username"] == "alice"
    assert d["role"] == "admin"

def test_order_total():
    item = OrderItem(product_id=1, product_name="Widget", quantity=3, unit_price=10.0)
    assert item.total == 30.0

def test_order_calculate_total():
    order = Order(id=1, user_id=1)
    order.items = [
        OrderItem(product_id=1, product_name="Widget", quantity=2, unit_price=10.0),
        OrderItem(product_id=2, product_name="Gadget", quantity=1, unit_price=25.0),
    ]
    assert order.calculate_total() == 45.0
