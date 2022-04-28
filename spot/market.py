from binance.spot import Spot as Client
from dotenv import load_dotenv
import os

load_dotenv()

key = os.environ["BNC_KEY"]
secret = os.environ["BNC_SECRET"]

client = Client(key, secret)


def get_current_price(symbol):
    depth = client.depth(symbol, limit = 10)
    return (float(depth['bids'][0][0]) + float(depth['asks'][0][0])) / 2