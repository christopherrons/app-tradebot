import asyncio
import websockets
import json
import ast

from TradebotUtils import TradeBotUtils


# Use class for api calls after testing is done
class BitstampApiAction:

    def __init__(self, bitstamp_token, market):
        self.__bitstamp_token = bitstamp_token
        self.__uri = "wss://ws.bitstamp.net/"
        self.__subscription = {
            "event": "bts:subscribe",
            "data": {
                "channel": f"order_book_{market}"
            }
        }

    def get_market_ask_price(self):
        return asyncio.get_event_loop().run_until_complete(self.async_get_market_ask_price())

    async def async_get_market_ask_price(self):

        async with websockets.connect(self.__uri) as websocket:
            await websocket.send(json.dumps(self.__subscription))

            data = ast.literal_eval(await websocket.recv())
            while data['data'] == {}:
                data = ast.literal_eval(await websocket.recv())

            market_ask_price = float(data['data']['asks'][0][0])
            market_ask_quantity = float(data['data']['asks'][0][1])
            return market_ask_price, market_ask_quantity

    def get_market_bid_price(self):
        return asyncio.get_event_loop().run_until_complete(self.async_get_market_bid_price())

    async def async_get_market_bid_price(self):

        async with websockets.connect(self.__uri) as websocket:
            await websocket.send(json.dumps(self.__subscription))

            data = ast.literal_eval(await websocket.recv())
            while data['data'] == {}:
                data = ast.literal_eval(await websocket.recv())

            market_bid_price = float(data['data']['bids'][0][0])
            market_bid_quantity = float(data['data']['bids'][0][1])
            return market_bid_price, market_bid_quantity

    def check_order_status(self):
        pass

    def sell_action(self):
        pass

    def buy_action(self):
        pass