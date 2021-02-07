from datetime import datetime
from TradeBotCache import TradeBotCache
from TradeBotOutput import TradeBotOutput
from BitstampApiAction import BitstampApiAction


class TradeBot:

    def __init__(self,
                 bitstamp_token,
                 market,
                 is_reset_logs,
                 trade_bot_cache,
                 is_buy=True):

        self._bitstamp_api = BitstampApiAction(bitstamp_token, market)
        self._is_buy = is_buy
        self._trade_bot_cache = trade_bot_cache
        self._trade_bot_output = TradeBotOutput(self._trade_bot_cache, is_reset_logs)

    def is_trade_able(self):
        if self._is_buy:
            market_ask_price, market_ask_quantity = self.get_market_ask_price()
            return self._trade_bot_cache.account_bid_price >= market_ask_price and \
                   self._trade_bot_cache.buy_quantity <= market_ask_quantity
        else:
            market_bid_price, market_bid_quantity = self.get_market_bid_price()
            return self._trade_bot_cache.account_ask_price <= market_bid_price and \
                   self._trade_bot_cache.buy_quantity <= market_bid_quantity

    def get_market_ask_price(self):
        market_ask_price, market_ask_quantity = self._bitstamp_api.get_market_ask_price()
        self._trade_bot_cache.market_ask_price = market_ask_price
        return market_ask_price, market_ask_quantity

    def get_market_bid_price(self):
        market_bid_price, market_bid_quantity = self._bitstamp_api.get_market_bid_price()
        self._trade_bot_cache.market_bid_price = market_bid_price
        return market_bid_price, market_bid_quantity

    def update_account_prices(self):
        if self._is_buy:
            self._trade_bot_cache._account_bid_price = self._trade_bot_cache.market_ask_price / (
                    1 + self._trade_bot_cache.interest)  # or always buy at the same price
        else:
            self._trade_bot_cache._account_ask_price = self._trade_bot_cache.market_bid_price * (
                    1 + self._trade_bot_cache.interest)
