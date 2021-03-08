from abc import ABC, abstractmethod

from services.algorithmic_trading.src.main.tradebots.TradeBotKing import TradeBotKing


class TradeBotSeller(TradeBotKing, ABC):

    def __init__(self, exchange_websocket, trade_bot_cache):
        super().__init__(exchange_websocket, trade_bot_cache)

    @abstractmethod
    def create_trade(self): pass

    @abstractmethod
    def trade_action_sell(self): pass

    @abstractmethod
    def update_account_values(self): pass

    def is_trade_able(self):
        market_bid_price = self.get_market_bid_price()
        market_bid_quantity = self._exchange_websocket.get_market_bid_quantity()
        return self._trade_bot_cache.account_ask_price <= market_bid_price and \
               self._trade_bot_cache.sell_quantity <= market_bid_quantity

    def get_market_bid_price(self):
        market_bid_price = self._exchange_websocket.get_market_bid_price()
        self._trade_bot_cache.market_bid_price = market_bid_price
        return market_bid_price

    def is_buy(self):
        return False

    def update_bid_price(self):
        self._trade_bot_cache.account_bid_price = self._trade_bot_cache.market_bid_price / (
                1 + self._trade_bot_cache.interest)
