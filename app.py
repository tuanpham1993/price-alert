import sys
sys.path.insert(0, './lib')

from dotenv import load_dotenv
from src.telegram import sendMessage
import os
from binance.websocket.spot.websocket_client import SpotWebsocketClient as WebsocketClient


load_dotenv()

threshold = float(os.environ['THRESHOLD'])
symbols = os.environ['SYMBOLS'].split(',')


cPrices = {}


def message_handler(message, symbol):
    if 'bids' in message and 'asks' in message:
        highestBid = float(message['bids'][0][0])
        lowestAsk = float(message['asks'][0][0])
        avgPrice = (highestBid + lowestAsk) / 2

        if cPrices[symbol] == 0:
            cPrices[symbol] = avgPrice

        if abs((avgPrice / cPrices[symbol] - 1) * 100) > threshold:
            if avgPrice  > cPrices[symbol]:
                icon = u"\U0001F680"
            else:
                icon = u"\U0001F53B"
            cPrices[symbol] = avgPrice
            sendMessage(icon + " " + symbol + " to " + str(avgPrice))


ws_client = WebsocketClient()
ws_client.start()

i = 0
for symbol in symbols:
    s = symbol
    cPrices[symbol] = 0

    ws_client.partial_book_depth(
        symbol,
        level=10,
        speed=1000,
        id=i,
        callback=lambda message, symbol=symbol: message_handler(
            message, symbol)
    )
    i += 1
