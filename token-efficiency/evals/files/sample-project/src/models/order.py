from dataclasses import dataclass, field
from datetime import datetime
from typing import List

@dataclass
class OrderItem:
    product_id: int
    product_name: str
    quantity: int
    unit_price: float

    @property
    def total(self):
        return self.quantity * self.unit_price

@dataclass
class Order:
    id: int
    user_id: int
    items: List[OrderItem] = field(default_factory=list)
    status: str = "pending"
    total: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)

    def calculate_total(self):
        self.total = sum(item.total for item in self.items)
        return self.total

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "items": [{"product_id": i.product_id, "product_name": i.product_name, "quantity": i.quantity, "unit_price": i.unit_price} for i in self.items],
            "status": self.status,
            "total": self.total,
            "created_at": self.created_at.isoformat(),
        }
