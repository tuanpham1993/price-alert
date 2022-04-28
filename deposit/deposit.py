import time
import functools
from binance.spot import Spot as Client
from dotenv import load_dotenv
import os

load_dotenv()

key = os.environ["BNC_KEY"]
secret = os.environ["BNC_SECRET"]

client = Client(key, secret)

def calc_deposit():
    remi_in = 98009551

    start = int(time.time() * 1000 - 2000000000)
    end = int(time.time() * 1000)

    buy = get_orders('BUY', start, end)
    sell = get_orders('SELL', start, end)

    buy_budget = functools.reduce(lambda a, b: a + float(b['totalPrice']), buy, 0)
    sell_budget = functools.reduce(lambda a, b: a + float(b['totalPrice']), sell, 0)

    return int(buy_budget - sell_budget + remi_in)

def get_orders(type, start, end):
    if start < 1577836800000: # Begin of 2020
        return []
 
    res = client.c2c_trade_history(type, startTimestamp = start, endTimestamp = end)
    orders = res['data']
    filled = list(filter(lambda x: x['orderStatus'] == 'COMPLETED', orders))
    prev = get_orders(type, start - 2000000000, start)
    filled.extend(prev)

    return filled
