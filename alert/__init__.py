
# ws_client = WebsocketClient()
# ws_client.start()

# i = 0
# for symbol in symbols:
#     s = symbol
#     cPrices[symbol] = 0

#     ws_client.partial_book_depth(
#         symbol,
#         level=10,
#         speed=1000,
#         id=i,
#         callback=lambda message, symbol=symbol: message_handler(
#             message, symbol)
#     )
#     i += 1