from asyncio import sleep

class CharacteristicsAnalyzer:
    def __init__(self):
        pass

    async def analyze(self, match, incoming_order) -> bool:
        await sleep(0.01)
        return match["price"] == incoming_order.price and match["status"] == "open"
        