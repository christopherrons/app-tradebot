from datetime import datetime
from TradeBotCache import TradeBotCache
from TradeBotOutput import TradeBotOutput


class TradeBot:

    def __init__(self,
                 account_bid_price,
                 interest,
                 initial_value,
                 bitstamp_token,
                 is_reinvesting_profits,
                 is_reset_logs,
                 is_buy=True):

        self._bitstamp_token = bitstamp_token
        self._is_buy = is_buy
        self._trade_bot_cache = TradeBotCache(initial_value, interest, account_bid_price, is_reinvesting_profits)
        self._trade_bot_output = TradeBotOutput(self._trade_bot_cache, is_reset_logs)

    def is_trade_able(self):
        if self._is_buy:
            return self._trade_bot_cache.account_bid_price >= self.get_market_ask_price()  # Make sure we dont buy to low e.g buy price = 100 and  ask price = 500.
        else:
            return self._trade_bot_cache.account_ask_price <= self.get_market_bid_price()

    def get_market_ask_price(self):
        market_ask_price = 0.3  ## temp
        self._trade_bot_cache.market_ask_price = market_ask_price
        return market_ask_price

    def get_market_bid_price(self):
        market_bid_price = 1  # temp
        self._trade_bot_cache.market_bid_price = market_bid_price
        return market_bid_price

    def update_account_prices(self):
        if self._is_buy:
            self._trade_bot_cache._account_bid_price = self._trade_bot_cache.market_ask_price / (
                    1 + self._trade_bot_cache.interest)  # or always buy at the same price
        else:
            self._trade_bot_cache._account_ask_price = self._trade_bot_cache.market_bid_price * (
                    1 + self._trade_bot_cache.interest)
