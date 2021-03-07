import ast
import asyncio
import json

import websockets

from Services.Runner.Exchange.ExchangeWebsocket import ExchangeWebsocket


class BitstampWebsocket(ExchangeWebsocket):

    def __init__(self, cash_currency, crypto_currency):
        self.__uri = "wss://ws.bitstamp.net/"
        self.__subscription = {
            "event": "bts:subscribe",
            "data": {
                "channel": f"order_book_{crypto_currency.lower()}{cash_currency.lower()}"
            }
        }
        self.current_order_id = None

        self.__websocket = None
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.__async__connect())

    async def __async__connect(self):
        print("Attempting connection to {}".format(self.__uri))
        self.__websocket = await websockets.connect(self.__uri)
        print("Connected\n")

    def get_market_ask_quantity(self):
        return asyncio.get_event_loop().run_until_complete(self.async_get_market_ask_quantity())

    async def async_get_market_ask_quantity(self):
        await self.__websocket.send(json.dumps(self.__subscription))

        data = ast.literal_eval(await self.__websocket.recv())
        while data['data'] == {}:
            data = ast.literal_eval(await self.__websocket.recv())

        market_ask_quantity = float(data['data']['asks'][0][1])
        return market_ask_quantity

    def get_market_bid_quantity(self):
        return asyncio.get_event_loop().run_until_complete(self.async_get_market_bid_quantity())

    async def async_get_market_bid_quantity(self):
        await self.__websocket.send(json.dumps(self.__subscription))

        data = ast.literal_eval(await self.__websocket.recv())
        while data['data'] == {}:
            data = ast.literal_eval(await self.__websocket.recv())

        market_bid_quantity = float(data['data']['bids'][0][1])
        return market_bid_quantity

    def get_market_ask_price(self):
        return asyncio.get_event_loop().run_until_complete(self.async_get_market_ask_price())

    async def async_get_market_ask_price(self):
        await self.__websocket.send(json.dumps(self.__subscription))

        data = ast.literal_eval(await self.__websocket.recv())
        while data['data'] == {}:
            data = ast.literal_eval(await self.__websocket.recv())

        return float(data['data']['asks'][0][0])

    def get_market_bid_price(self):
        return asyncio.get_event_loop().run_until_complete(self.async_get_market_bid_price())

    async def async_get_market_bid_price(self):
        await self.__websocket.send(json.dumps(self.__subscription))

        data = ast.literal_eval(await self.__websocket.recv())
        while data['data'] == {}:
            data = ast.literal_eval(await self.__websocket.recv())

        return float(data['data']['bids'][0][0])
