import asyncio
import json

from applications.common.src.main.exchanges.ExchangeWebsocket import ExchangeWebsocket


class KrakenWebsocket(ExchangeWebsocket):

    def __init__(self, cash_currency, crypto_currency):
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

        super().__init__(exchange_name="kraken",
                         cash_currency=cash_currency,
                         crypto_currency=crypto_currency,
                         uri="wss://ws.kraken.com/")

    def get_market_ask_order(self) -> tuple:
        return asyncio.get_event_loop().run_until_complete(self.__async_get_market_ask_order())

    async def __async_get_market_ask_order(self) -> tuple:
        await self._websocket.send(json.dumps(self.__subscription))

        while True:
            data = json.loads(await self._websocket.recv())
            if isinstance(data, list) and isinstance(data[1], dict) and 'as' in data[1].keys():
                break

        market_ask_quantity = float(data[self.__ask_dictionary_index]['as'][self.__best_price_index][self.__quantity_index])
        market_ask_price = float(data[self.__ask_dictionary_index]['as'][self.__best_price_index][self.__price_index])
        return market_ask_price, market_ask_quantity

    def get_market_bid_order(self) -> tuple:
        return asyncio.get_event_loop().run_until_complete(self.__async_get_market_bid_order())

    async def __async_get_market_bid_order(self) -> tuple:
        await self._websocket.send(json.dumps(self.__subscription))

        while True:
            data = json.loads(await self._websocket.recv())
            if isinstance(data, list) and isinstance(data[1], dict) and 'bs' in data[1].keys():
                break

        market_bid_quantity = float(data[self.__bid_dictionary_index]['bs'][self.__best_price_index][self.__quantity_index])
        market_bid_price = float(data[self.__bid_dictionary_index]['bs'][self.__best_price_index][self.__price_index])
        return market_bid_price, market_bid_quantity

    def get_market_bid_price(self) -> float:
        return self.get_market_bid_order()[0]

    def get_market_bid_quantity(self) -> float:
        return self.get_market_bid_order()[1]

    def get_market_ask_price(self) -> float:
        return self.get_market_ask_order()[0]

    def get_market_ask_quantity(self) -> float:
        return self.get_market_ask_order()[1]
