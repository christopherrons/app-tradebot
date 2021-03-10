from abc import ABC, abstractmethod


class ExchangeWebsocket(ABC):

    @abstractmethod
    def get_market_ask_quantity(self) -> float: pass

    @abstractmethod
    def get_market_bid_quantity(self) -> float: pass

    @abstractmethod
    def get_market_ask_price(self) -> float: pass

    @abstractmethod
    def get_market_bid_price(self) -> float: pass

    @property
    @abstractmethod
    def exchange_name(self) -> str: pass

    @exchange_name.setter
    @abstractmethod
    def exchange_name(self, exchange_name: str): pass

    @property
    @abstractmethod
    def cash_currency(self) -> str: pass

    @cash_currency.setter
    @abstractmethod
    def cash_currency(self, cash_currency: str): pass

    @property
    @abstractmethod
    def crypto_currency(self) -> str: pass

    @crypto_currency.setter
    @abstractmethod
    def crypto_currency(self, crypto_currency): pass
