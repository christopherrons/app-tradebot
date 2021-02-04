from TradeBotCache import TradeBotCache
from TradeBotOutput import TradeBotOutput
from TradebotUtils import TradeBotUtils
import time
from datetime import datetime, timedelta


class CryptoTradeBot:

    def __init__(self, account_bid_price, interest, initial_value, bitstamp_token, run_time_minutes,
                 is_reinvesting_profits,
                 is_simulation, is_buy=True):
        self.account_bid_price = account_bid_price
        self.run_stop_time = datetime.now() + timedelta(seconds=(run_time_minutes * 60))
        self.initial_value = initial_value
        self.bitstamp_token = bitstamp_token
        self.is_simulation = is_simulation
        self.is_buy = is_buy
        self.account_ask_price = (1 + interest) * account_bid_price

        self.trade_bot_cache = TradeBotCache(initial_value, interest, is_reinvesting_profits)
        self.trade_bot_output = TradeBotOutput(self.trade_bot_cache)

    def run(self):
        "Runner"
        start_time = datetime.now()
        while True:
            self.trade_decision_algorithm()
            ## here we shiould print some market data from time to time

            if TradeBotUtils.is_run_time_passed(datetime.now(), self.run_stop_time):
                break

        print(f"Starting trading at {start_time} and ended at {datetime.now()}")

    def get_market_ask_price(self):
        "Gets the current ask price of the crypto currency"
        market_ask_price = 1
        self.trade_bot_cache.set_market_ask_price(market_ask_price)
        return market_ask_price

    def get_market_bid_price(self):
        "Gets the current bid price of the crypto currency"
        market_bid_price = 1
        self.trade_bot_cache.set_market_bid_price(market_bid_price)
        return market_bid_price

    def trade_decision_algorithm(self):
        "Decision to buy or sell"
        if self.is_buy:
            if self.account_bid_price >= self.get_market_ask_price():  # Make sure we dont buy to low e.g buy price = 100 and  ask price = 500.
                self.trade_action_buy()  # If the price goes below the initial buy price the by some delta then we should adjust the buy and sell price
        else:
            if self.account_ask_price == self.get_market_bid_price():
                self.trade_action_sell()

    def trade_action_buy(self):
        "Http-request to Bistamp API"
        if not self.is_simulation:
            if self.is_successful_trade():
                pass

        self.is_buy = False
        self.update_cache_account_prices()

    def trade_action_sell(self):
        "Http-request to Bistamp API"
        if not self.is_simulation:
            if self.is_successful_trade():
                pass
        self.is_buy = True

        self.trade_bot_cache.set_successful_cycles()
        self.update_cache_account_prices()

    def is_successful_trade(self):
        "checks if the trades has gone through"
        pass

    def update_cache_account_prices(self):
        if self.is_buy:
            self.trade_bot_cache.set_account_bid_price(self.account_bid_price)
        else:
            self.trade_bot_cache.set_account_ask_price(self.account_ask_price)
