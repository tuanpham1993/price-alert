from binance.spot import Spot as Client
import spot.market as spot_market
import margin.order as margin_order
from dotenv import load_dotenv
import os

load_dotenv()

key = os.environ["BNC_KEY"]
secret = os.environ["BNC_SECRET"]

client = Client(key, secret)


def calc_position(num_orders, symbol = 'CAKEBTC'):
    current_price = spot_market.get_current_price(symbol)
    orders = margin_order.get_orders(num_orders, symbol)

    num_buy_orders = 0
    num_sell_orders = 0

    buy_qty = 0
    sell_qty = 0

    buy_budget = 0
    sell_budget = 0

    for order in orders:
        if order['side'] == 'BUY':
            num_buy_orders += 1
            buy_qty += float(order["executedQty"])
            buy_budget += float(order["cummulativeQuoteQty"])

        elif order['side'] == 'SELL':
            num_sell_orders += 1
            sell_qty += float(order["executedQty"])
            sell_budget += float(order["cummulativeQuoteQty"])

    diff_buy_sell_budget = buy_budget - sell_budget
    diff_buy_sell_qty = buy_qty - sell_qty

    if diff_buy_sell_qty != 0:
        avg_price = diff_buy_sell_budget / diff_buy_sell_qty
        profit = (current_price/avg_price - 1) * diff_buy_sell_qty
    else:
        avg_price = 0
        profit = -diff_buy_sell_budget / current_price

    result = {
        'avgPrice': avg_price,
        'qty': diff_buy_sell_qty,
        'profit': profit
    }

    if diff_buy_sell_qty > 0:
        result['side'] = 'BUY'
    elif diff_buy_sell_qty < 0:
        result['side'] = 'SELL'
    else:
        result = {
            'profit': profit
        }

    return result
