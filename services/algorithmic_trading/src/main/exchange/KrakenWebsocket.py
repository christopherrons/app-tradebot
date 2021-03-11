import asyncio
import json

import websockets

from services.algorithmic_trading.src.main.exchange.ExchangeWebsocket import ExchangeWebsocket


class KrakenWebsocket(ExchangeWebsocket):

    def __init__(self, cash_currency, crypto_currency):
        self.__cash_currency = cash_currency
        self.__crypto_currency = crypto_currency
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

        self.__exchange_name = "Kraken"
        self.__websocket = None
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.__async__connect())

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

    @property
    def exchange_name(self) -> str:
        return self.__exchange_name

    @exchange_name.setter
    def exchange_name(self, exchange_name: str):
        self.__exchange_name = exchange_name

    @property
    def cash_currency(self) -> str:
        return self.__cash_currency

    @cash_currency.setter
    def cash_currency(self, cash_currency: str):
        self.__cash_currency = cash_currency

    @property
    def crypto_currency(self) -> str:
        return self.__crypto_currency

    @crypto_currency.setter
    def crypto_currency(self, crypto_currency):
        self.__crypto_currency = crypto_currency
