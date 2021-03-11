from abc import ABC, abstractmethod

from services.algorithmic_trading.src.main.exchange.ExchangeService import ExchangeService


class ExchangeWebsocket(ExchangeService, ABC):

    def __init__(self, exchange_name: str, cash_currency: str, crypto_currency: str):
        super().__init__(exchange_name, cash_currency, crypto_currency)

    @abstractmethod
    def get_market_ask_quantity(self) -> float: pass

    @abstractmethod
    def get_market_bid_quantity(self) -> float: pass

    @abstractmethod
    def get_market_ask_price(self) -> float: pass

    @abstractmethod
    def get_market_bid_price(self) -> float: pass
