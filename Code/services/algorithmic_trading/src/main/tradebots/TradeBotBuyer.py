from abc import ABC, abstractmethod

from services.algorithmic_trading.src.main.cache_storage.TradeBotCache import TradeBotCache
from services.algorithmic_trading.src.main.exchange.ExchangeWebsocket import ExchangeWebsocket
from services.algorithmic_trading.src.main.tradebots.TradeBot import TradeBot


class TradeBotBuyer(TradeBot, ABC):

    def __init__(self,
                 exchange_websocket: ExchangeWebsocket,
                 trade_bot_cache: TradeBotCache):
        super().__init__(exchange_websocket, trade_bot_cache)

    @abstractmethod
    def trade_action_buy(self) -> str: pass

    def is_trade_able(self) -> bool:
        market_ask_price = self.get_market_ask_price()
        market_ask_quantity = self._exchange_websocket.get_market_ask_quantity()
        return self._trade_bot_cache.account_bid_price >= market_ask_price and \
               self._trade_bot_cache.buy_quantity <= market_ask_quantity

    def get_market_ask_price(self) -> float:
        market_ask_price = self._exchange_websocket.get_market_ask_price()
        self._trade_bot_cache.market_ask_price = market_ask_price
        return market_ask_price

    def is_buy(self) -> bool:
        return True

    def update_ask_price(self):
        self._trade_bot_cache.account_ask_price = self._trade_bot_cache.market_ask_price * (
                1 + self._trade_bot_cache.interest)
