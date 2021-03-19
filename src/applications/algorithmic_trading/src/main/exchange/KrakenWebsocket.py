import asyncio
import json

import websockets

from applications.algorithmic_trading.src.main.exchange.ExchangeWebsocket import ExchangeWebsocket


class KrakenWebsocket(ExchangeWebsocket):

    def __init__(self, cash_currency, crypto_currency):
        self.__uri = "wss://ws.kraken.com/"
        self.__subscription = {
            "event": "subscribe",
            "pair": [f"{crypto_currency.upper()}/{cash_currency.upper()}"],
            "subscription": {"name": "book"}
        }
        self.__ask_dictionary_index = 1
        self.__bid_dictionary_index = 1
        self.__price_index = 0
        self.__quantity_index = 1
        self.__best_price_index = 0

        self.__websocket = None
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.__async__connect())

        super().__init__("kraken", cash_currency, crypto_currency)

    async def __async__connect(self):
        print("Attempting connection to {}".format(self.__uri))
        self.__websocket = await websockets.connect(self.__uri)
        print("Connected\n")

    def get_market_ask_quantity(self) -> float:
        return asyncio.get_event_loop().run_until_complete(self.__async_get_market_ask_quantity())

    async def __async_get_market_ask_quantity(self) -> float:
        await self.__websocket.send(json.dumps(self.__subscription))

        while True:
            data = json.loads(await self.__websocket.recv())
            if isinstance(data, list) and isinstance(data[1], dict) and 'as' in data[1].keys():
                break

        market_bid_quantity = float(
            data[self.__ask_dictionary_index]['as'][self.__best_price_index][self.__quantity_index])
        return market_bid_quantity

    def get_market_bid_quantity(self) -> float:
        return asyncio.get_event_loop().run_until_complete(self.__async_get_market_bid_quantity())

    async def __async_get_market_bid_quantity(self) -> float:
        await self.__websocket.send(json.dumps(self.__subscription))

        while True:
            data = json.loads(await self.__websocket.recv())
            if isinstance(data, list) and isinstance(data[1], dict) and 'bs' in data[1].keys():
                break

        market_bid_quantity = float(
            data[self.__bid_dictionary_index]['bs'][self.__best_price_index][self.__quantity_index])
        return market_bid_quantity

    def get_market_ask_price(self) -> float:
        return asyncio.get_event_loop().run_until_complete(self.__async_get_market_ask_price())

    async def __async_get_market_ask_price(self) -> float:
        await self.__websocket.send(json.dumps(self.__subscription))

        while True:
            data = json.loads(await self.__websocket.recv())
            if isinstance(data, list) and isinstance(data[1], dict) and 'as' in data[1].keys():
                break

        return float(data[self.__ask_dictionary_index]['as'][self.__best_price_index][self.__price_index])

    def get_market_bid_price(self) -> float:
        return asyncio.get_event_loop().run_until_complete(self.__async_get_market_bid_price())

    async def __async_get_market_bid_price(self) -> float:
        await self.__websocket.send(json.dumps(self.__subscription))

        while True:
            data = json.loads(await self.__websocket.recv())
            if isinstance(data, list) and isinstance(data[1], dict) and 'bs' in data[1].keys():
                break

        return float(data[self.__bid_dictionary_index]['bs'][self.__best_price_index][self.__price_index])
