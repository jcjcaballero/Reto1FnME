import azure.functions as func
import logging
import json
import os
from azure.cosmos import CosmosClient
from models.order import Order
from services.matching_service import MatchingService

app = func.FunctionApp()
cosmos_db_connection_string = os.getenv("l_cosmos_db_connection_string")
client = CosmosClient.from_connection_string(cosmos_db_connection_string)
matcher = MatchingService(client)

@app.service_bus_queue_trigger(arg_name="azservicebus", queue_name="ordenescompraventa",
                               connection="sbreto1as_SERVICEBUS") 

async def motorEmparejamiento(azservicebus: func.ServiceBusMessage):
    order_data = json.loads(azservicebus.get_body().decode('utf-8'))
    order = Order.create_order(order_data)

    if await matcher.process_order(order):
        logging.info(f"Orden {order.id} emparejada correctamente")
    else:
        logging.info(f"No se encontró match para {order.id}, quedará abierta")