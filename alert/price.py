import os
from binance.websocket.spot.websocket_client import SpotWebsocketClient as WebsocketClient
from notification.telegram import sendMessage

ws_client = WebsocketClient()
ws_client.start()

prices = {}
threshold = float(os.environ['THRESHOLD'])

def alert_price():
    symbols = os.getenv('SYMBOLS').split(',')
    global prices

    for i, symbol in enumerate(symbols):
        prices[symbol] = 0

        ws_client.partial_book_depth(
            symbol,
            level=10,
            speed=1000,
            id=i,
            callback=lambda message, symbol=symbol: message_handler(
                message, symbol)
        )

def message_handler(message, symbol):
    global prices, threshold

    if 'bids' in message and 'asks' in message:
        highestBid = float(message['bids'][0][0])
        lowestAsk = float(message['asks'][0][0])
        avgPrice = (highestBid + lowestAsk) / 2

        if prices[symbol] == 0:
            prices[symbol] = avgPrice

        if abs((avgPrice / prices[symbol] - 1) * 100) > threshold:
            if avgPrice > prices[symbol]:
                icon = u"\U0001F680"
            else:
                icon = u"\U0001F53B"
            prices[symbol] = avgPrice
            sendMessage(icon + " " + symbol + " to " + str(avgPrice))