import asyncio
import json

import websockets


class KrakenWebsocket:

    def __init__(self):
        self.__uri = "wss://ws.kraken.com/"
        self.__subscription = {
            "event": "subscribe",
            "pair": ["XRP/USD"],
            "subscription": {"name": "book"}
        }
        self.__ask_dictionary_index = 1
        self.__bid_dictionary_index = 1
        self.__price_index = 0
        self.__quantity_index = 1
        self.__best_price_index = 0

    def get_market_ask_price_and_quantity(self):
        return asyncio.get_event_loop().run_until_complete(self.async_get_market_ask_price_and_quantity())

    async def async_get_market_ask_price_and_quantity(self):
        async with websockets.connect(self.__uri) as websocket:
            await websocket.send(json.dumps(self.__subscription))

            while True:
                data = json.loads(await websocket.recv())
                if isinstance(data, list) and isinstance(data[1], dict) and 'as' in data[1].keys():
                    break

            market_bid_price = float(
                data[self.__ask_dictionary_index]['as'][self.__best_price_index][self.__price_index])
            market_bid_quantity = float(
                data[self.__ask_dictionary_index]['as'][self.__best_price_index][self.__quantity_index])
            return market_bid_price, market_bid_quantity

    def get_market_bid_price_and_quantity(self):
        return asyncio.get_event_loop().run_until_complete(self.async_get_market_bid_price_and_quantity())

    async def async_get_market_bid_price_and_quantity(self):
        async with websockets.connect(self.__uri) as websocket:
            await websocket.send(json.dumps(self.__subscription))

            while True:
                data = json.loads(await websocket.recv())
                if isinstance(data, list) and isinstance(data[1], dict) and 'bs' in data[1].keys():
                    break

            market_bid_price = float(
                data[self.__bid_dictionary_index]['bs'][self.__best_price_index][self.__price_index])
            market_bid_quantity = float(
                data[self.__bid_dictionary_index]['bs'][self.__best_price_index][self.__quantity_index])
            return market_bid_price, market_bid_quantity

    def get_market_ask_price(self):
        return asyncio.get_event_loop().run_until_complete(self.async_get_market_ask_price())

    async def async_get_market_ask_price(self):
        async with websockets.connect(self.__uri) as websocket:
            await websocket.send(json.dumps(self.__subscription))

            while True:
                data = json.loads(await websocket.recv())
                if isinstance(data, list) and isinstance(data[1], dict) and 'as' in data[1].keys():
                    break

            return float(data[self.__ask_dictionary_index]['as'][self.__best_price_index][self.__price_index])

    def get_market_bid_price(self):
        return asyncio.get_event_loop().run_until_complete(self.async_get_market_bid_price())

    async def async_get_market_bid_price(self):
        async with websockets.connect(self.__uri) as websocket:
            await websocket.send(json.dumps(self.__subscription))

            while True:
                data = json.loads(await websocket.recv())
                if isinstance(data, list) and isinstance(data[1], dict) and 'bs' in data[1].keys():
                    break

            return float(data[self.__bid_dictionary_index]['bs'][self.__best_price_index][self.__price_index])
