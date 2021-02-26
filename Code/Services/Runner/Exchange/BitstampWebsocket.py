import ast
import asyncio
import json
import websockets


class BitstampWebsocket:

    def __init__(self):
        self.__uri = "wss://ws.bitstamp.net/"
        self.__subscription = {
            "event": "bts:subscribe",
            "data": {
                "channel": "order_book_xrpusd"
            }
        }
        self.current_order_id = None

    def get_market_ask_price_and_quantity(self):
        return asyncio.get_event_loop().run_until_complete(self.async_get_market_ask_price_and_quantity())

    async def async_get_market_ask_price_and_quantity(self):
        async with websockets.connect(self.__uri) as websocket:
            await websocket.send(json.dumps(self.__subscription))

            data = ast.literal_eval(await websocket.recv())
            while data['data'] == {}:
                data = ast.literal_eval(await websocket.recv())

            market_ask_price = float(data['data']['asks'][0][0])
            market_ask_quantity = float(data['data']['asks'][0][1])
            return market_ask_price, market_ask_quantity

    def get_market_bid_price_and_quantity(self):
        return asyncio.get_event_loop().run_until_complete(self.async_get_market_bid_price_and_quantity())

    async def async_get_market_bid_price_and_quantity(self):
        async with websockets.connect(self.__uri) as websocket:
            await websocket.send(json.dumps(self.__subscription))

            data = ast.literal_eval(await websocket.recv())
            while data['data'] == {}:
                data = ast.literal_eval(await websocket.recv())

            market_bid_price = float(data['data']['bids'][0][0])
            market_bid_quantity = float(data['data']['bids'][0][1])
            return market_bid_price, market_bid_quantity

    def get_market_ask_price(self):
        return asyncio.get_event_loop().run_until_complete(self.async_get_market_ask_price())

    async def async_get_market_ask_price(self):
        async with websockets.connect(self.__uri) as websocket:
            await websocket.send(json.dumps(self.__subscription))

            data = ast.literal_eval(await websocket.recv())
            while data['data'] == {}:
                data = ast.literal_eval(await websocket.recv())

            return float(data['data']['asks'][0][0])

    def get_market_bid_price(self):
        return asyncio.get_event_loop().run_until_complete(self.async_get_market_bid_price())

    async def async_get_market_bid_price(self):
        async with websockets.connect(self.__uri) as websocket:
            await websocket.send(json.dumps(self.__subscription))

            data = ast.literal_eval(await websocket.recv())
            while data['data'] == {}:
                data = ast.literal_eval(await websocket.recv())

            return float(data['data']['bids'][0][0])
