from abc import ABC, abstractmethod


class ExchangeWebsocket(ABC):

    @abstractmethod
    def get_market_ask_quantity(self): pass

    @abstractmethod
    def get_market_bid_quantity(self): pass

    @abstractmethod
    def get_market_ask_price(self): pass

    @abstractmethod
    def get_market_bid_price(self): pass
