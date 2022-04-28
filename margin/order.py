from binance.spot import Spot as Client
from dotenv import load_dotenv
import os

load_dotenv()

key = os.environ["BNC_KEY"]
secret = os.environ["BNC_SECRET"]

client = Client(key, secret)

def get_orders(num_orders, symbol):
    client = Client(key, secret)

    orders = client.margin_all_orders(symbol)
    orders.reverse()

    filled_orders = list(filter(lambda x: x['status'] in ['FILLED', 'PARTIALLY_FILLED'], orders))
    return filled_orders[:num_orders]
