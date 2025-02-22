import logging
from services.order_repository import OrderRepository

class MatchingService:
    def __init__(self):
        self.order_repo = OrderRepository()

    def process_order(self, incoming_order):
        opposite_type = "buy" if incoming_order.type == "sell" else "sell"
        matching_orders = self.order_repo.get_orders_by_type(incoming_order.assetSymbol, opposite_type)

        for match in matching_orders:
            if match["price"] == incoming_order.price and match["status"] == "open":
                logging.info(f"Match encontrado entre {incoming_order.id} y {match['id']}")

                # Actualizar órdenes en CosmosDB
                self.order_repo.update_order(match["id"], {"status": "matched", "matching": incoming_order.__dict__, "partitionKey": match["partitionKey"]})
                self.order_repo.update_order(incoming_order.id, {"status": "matched", "matching": match, "partitionKey": incoming_order.partitionKey})

                return True

        return False
