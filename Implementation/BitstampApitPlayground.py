import asyncio
import websockets
import json
import ast

from TradebotUtils import TradeBotUtils

# Use class for api calls after testing is done
class BitstampApiPlayground:

    def __init__(self):
        self.bitstamp_token = TradeBotUtils.get_bitstamp_token()
        self.uri = "wss://ws.bitstamp.net/"
        self.subscription = {
                "event": "bts:subscribe",
                "data": {
                    "channel": "order_book_xrpusd"
                }
            }

    async def get_market_ask_price(self):

        async with websockets.connect(self.uri) as websocket:
            await websocket.send(json.dumps(self.subscription))

            data = ast.literal_eval(await websocket.recv())

            while data['data'] == {}:
                data = ast.literal_eval(await websocket.recv())

            return data['data']['asks'][0]

    asyncio.get_event_loop().run_until_complete(get_market_ask_price())

    async def get_market_bid_price(self):

        async with websockets.connect(self.uri) as websocket:
            await websocket.send(json.dumps(self.subscription))

            data = ast.literal_eval(await websocket.recv())

            while data['data'] == {}:
                data = ast.literal_eval(await websocket.recv())

            return data['data']['bids'][0]

    asyncio.get_event_loop().run_until_complete(get_market_bid_price())

    def check_order_status(self):
        pass

    def sell_action(self):
        pass

    def buy_action(self):
        pass
