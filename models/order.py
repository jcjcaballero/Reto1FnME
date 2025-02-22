from dataclasses import dataclass
import uuid
from datetime import datetime, timezone

@dataclass
class Order:
    id: str
    type: str  # "buy" o "sell"
    assetSymbol: str
    quantity: int
    price: float
    status: str  # "open", "matched"
    created_at: str
    updated_at: str
    user_id: str
    matching: dict | None
    partitionKey: str

    @staticmethod
    def create_order(order_data):
        return Order(
            id=order_data.get("id", str(uuid.uuid4())),
            type=order_data["type"],
            assetSymbol=order_data["assetSymbol"],
            quantity=order_data["quantity"],
            price=order_data["price"],
            status=order_data.get("status", "open"),
            created_at=order_data.get("created_at", datetime.now(timezone.utc).isoformat()),
            updated_at=datetime.now(timezone.utc).isoformat(),
            user_id=order_data["user_id"],
            matching=order_data.get("matching"),
            partitionKey=order_data["assetSymbol"],
        )
