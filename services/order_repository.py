from azure.cosmos import CosmosClient
import os

class OrderRepository:
    def __init__(self):
        cosmos_db_connection_string = os.getenv("l_cosmos_db_connection_string")
        cosmos_db_name = os.getenv("l_cosmos_db_name")
        container_name = os.getenv("l_container_name")

        self.client = CosmosClient.from_connection_string(cosmos_db_connection_string)
        self.database = self.client.get_database_client(cosmos_db_name)
        self.container = self.database.get_container_client(container_name)

    def get_orders_by_type(self, asset_symbol, order_type):
        query = f"SELECT * FROM c WHERE c.assetSymbol = '{asset_symbol}' AND c.type = '{order_type}' AND c.status = 'open'"
        return list(self.container.query_items(query=query, enable_cross_partition_query=True))

    def update_order(self, order_id, update_data):
        order = self.container.read_item(item=order_id, partition_key=update_data["partitionKey"])
        for key, value in update_data.items():
            order[key] = value
        self.container.replace_item(order_id, order) 
