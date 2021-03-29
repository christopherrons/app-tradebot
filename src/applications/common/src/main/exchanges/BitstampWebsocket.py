import ast
import asyncio
import json

from applications.common.src.main.exchanges.ExchangeWebsocket import ExchangeWebsocket


class BitstampWebsocket(ExchangeWebsocket):

    def __init__(self, cash_currency: str, crypto_currency: str):
        self.__subscription = {
            "event": "bts:subscribe",
            "data": {
                "channel": f"order_book_{crypto_currency.lower()}{cash_currency.lower()}"
            }
        }

        super().__init__(exchange_name="bitstamp",
                         cash_currency=cash_currency,
                         crypto_currency=crypto_currency,
                         uri="wss://ws.bitstamp.net/")

    def get_market_ask_order(self) -> tuple:
        return asyncio.get_event_loop().run_until_complete(self.__async_get_market_ask_order())

    async def __async_get_market_ask_order(self) -> tuple:
        await self._websocket.send(json.dumps(self.__subscription))

        data = ast.literal_eval(await self._websocket.recv())
        while data['data'] == {}:
            data = ast.literal_eval(await self._websocket.recv())

        market_ask_quantity = float(data['data']['asks'][0][1])
        market_ask_price = float(data['data']['asks'][0][0])
        return market_ask_price, market_ask_quantity

    def get_market_bid_order(self) -> tuple:
        return asyncio.get_event_loop().run_until_complete(self.__async_get_market_bid_order())

    async def __async_get_market_bid_order(self) -> tuple:
        await self._websocket.send(json.dumps(self.__subscription))

        data = ast.literal_eval(await self._websocket.recv())
        while data['data'] == {}:
            data = ast.literal_eval(await self._websocket.recv())

        market_bid_quantity = float(data['data']['bids'][0][1])
        market_bid_price = float(data['data']['bids'][0][0])
        return market_bid_price, market_bid_quantity

    def get_market_bid_price(self) -> float:
        return self.get_market_bid_order()[0]

    def get_market_bid_quantity(self) -> float:
        return self.get_market_bid_order()[1]

    def get_market_ask_price(self) -> float:
        return self.get_market_bid_order()[0]

    def get_market_ask_quantity(self) -> float:
        return self.get_market_bid_order()[1]
