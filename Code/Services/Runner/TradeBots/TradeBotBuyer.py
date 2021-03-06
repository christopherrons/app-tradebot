from abc import ABC, abstractmethod

from Services.Runner.TradeBots.TradeBotKing import TradeBotKing


class TradeBotBuyer(TradeBotKing, ABC):

    def __init__(self, exchange_websocket, trade_bot_cache):
        super().__init__(exchange_websocket, trade_bot_cache)

    @abstractmethod
    def create_trade(self): pass

    @abstractmethod
    def trade_action_buy(self): pass

    @abstractmethod
    def update_account_values(self): pass

    def is_trade_able(self):
        market_ask_price = self.get_market_ask_price()
        market_ask_quantity = self._exchange_websocket.get_market_ask_quantity()
        return self._trade_bot_cache.account_bid_price >= market_ask_price and \
               self._trade_bot_cache.buy_quantity <= market_ask_quantity

    def get_market_ask_price(self):
        market_ask_price = self._exchange_websocket.get_market_ask_price()
        self._trade_bot_cache.market_ask_price = market_ask_price
        return market_ask_price

    def is_buy(self):
        return True

    def update_ask_price(self):
        self._trade_bot_cache.account_ask_price = self._trade_bot_cache.market_ask_price * (
                1 + self._trade_bot_cache.interest)
