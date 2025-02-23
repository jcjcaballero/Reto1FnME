import logging
from services.order_repository import OrderRepository
from services.characteristics_analyzer import CharacteristicsAnalyzer
from asyncio import gather

class MatchingService:
    def __init__(self):
        self.order_repo = OrderRepository()
        self.characteristics_analyzer = CharacteristicsAnalyzer()

    async def process_order(self, incoming_order):
        opposite_type = "buy" if incoming_order.type == "sell" else "sell"
        matching_orders = await self.order_repo.get_orders_by_type(incoming_order.assetSymbol, opposite_type)

        tasks = [
            self.process_match(incoming_order, match)
            for match in matching_orders
            if await self.characteristics_analyzer.analyze(match, incoming_order)
        ]
        
        results = await gather(*tasks)  # Run all tasks in parallel
        return any(results)
    
    
    async def process_match(self, incoming_order, match):
        logging.info(f"Match encontrado entre {incoming_order.id} y {match['id']}")
        await gather(
            self.order_repo.update_order(match["id"], {
                "status": "matched", "matching": incoming_order.__dict__, "partitionKey": match["partitionKey"]
            }),
            self.order_repo.update_order(incoming_order.id, {
                "status": "matched", "matching": match, "partitionKey": incoming_order.partitionKey
            })
        )
        return True    
