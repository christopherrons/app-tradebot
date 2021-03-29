import asyncio
from abc import ABC, abstractmethod

import websockets

from applications.common.src.main.exchanges.ExchangeService import ExchangeService
from applications.common.src.main.utils.PrinterUtils import PrinterUtils


class ExchangeWebsocket(ExchangeService, ABC):

    def __init__(self, exchange_name: str, cash_currency: str, crypto_currency: str, uri: str):
        super().__init__(exchange_name, cash_currency, crypto_currency)

        self._websocket = None
        self.__uri = uri
        self.__loop = asyncio.get_event_loop()
        self.__loop.run_until_complete(self.__async__connect())

    async def __async__connect(self):
        PrinterUtils.console_log(message="Attempting connection to {}".format(self.__uri))
        self._websocket = await websockets.connect(self.__uri)
        PrinterUtils.console_log(message=("Connected"))

    def reconnect(self):
        self.__loop = asyncio.get_event_loop()
        self.__loop.run_until_complete(self.__async__connect())

    @abstractmethod
    def get_market_ask_order(self) -> tuple: pass

    @abstractmethod
    def get_market_bid_order(self) -> tuple: pass

    @abstractmethod
    def get_market_bid_price(self) -> float: pass

    @abstractmethod
    def get_market_bid_quantity(self) -> float: pass

    @abstractmethod
    def get_market_ask_price(self) -> float: pass

    @abstractmethod
    def get_market_ask_quantity(self) -> float: pass
