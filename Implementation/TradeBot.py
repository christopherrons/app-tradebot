from TradeBotCache import TradeBotCache
from TradeBotOutput import TradeBotOutput
from TradebotUtils import TradeBotUtils
from datetime import datetime, timedelta


class CryptoTradeBot:

    def __init__(self, account_bid_price,
                 interest,
                 initial_value,
                 bitstamp_token,
                 run_time_minutes,
                 is_reinvesting_profits,
                 is_not_simulation,
                 print_interval,
                 is_reset_logs,
                 is_buy=True):

        self.account_bid_price = account_bid_price
        self.interest = interest
        self.run_stop_time = datetime.now() + timedelta(seconds=(run_time_minutes * 60))
        self.initial_value = initial_value
        self.bitstamp_token = bitstamp_token
        self.is_not_simulation = is_not_simulation
        self.print_interval = print_interval
        self.is_buy = is_buy
        self.account_ask_price = (1 + interest) * account_bid_price

        self.trade_bot_cache = TradeBotCache(initial_value, interest, is_reinvesting_profits)
        self.trade_bot_output = TradeBotOutput(self.trade_bot_cache, is_reset_logs)

    def run(self):
        start_time = datetime.now()
        print(f"Starting trading at {start_time}\n")

        delta_minutes = start_time
        while not TradeBotUtils.is_run_time_passed(datetime.now(), self.run_stop_time):

            if (datetime.now() - delta_minutes).seconds >= (self.print_interval * 60):
                self.trade_bot_output.print_and_log_data(self.is_buy)
                delta_minutes = datetime.now()
                self.is_buy = not self.is_buy  # remove after testing as this will change automatially

            self.trade_decision_algorithm()

        print(f"Started trading at {start_time} and ended at {datetime.now()}")

    def get_market_ask_price(self):
        market_ask_price = 1
        self.trade_bot_cache.set_market_ask_price(market_ask_price)
        return market_ask_price

    def get_market_bid_price(self):
        market_bid_price = 1
        self.trade_bot_cache.set_market_bid_price(market_bid_price)
        return market_bid_price

    def trade_decision_algorithm(self):
        if self.is_buy:
            if self.account_bid_price >= self.get_market_ask_price():  # Make sure we dont buy to low e.g buy price = 100 and  ask price = 500.
                self.trade_action_buy()  # If the price goes below the initial buy price the by some delta then we should adjust the buy and sell price
        else:
            if self.account_ask_price <= self.get_market_bid_price():
                self.trade_action_sell()

    def update_account_prices(self):
        if self.is_buy:
            self.account_bid_price = self.trade_bot_cache.get_market_bid_price() / (1 + self.interest)
            self.trade_bot_cache.set_account_bid_price(self.account_bid_price)
        else:
            self.account_ask_price = self.trade_bot_cache.get_market_ask_price() * (1 + self.interest)
            self.trade_bot_cache.set_account_ask_price(self.account_ask_price)


