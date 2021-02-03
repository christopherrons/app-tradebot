import math


class TradeBotCache:

    def __init__(self, initial_value, interest, is_reinvesting_profits):
        self.initial_value = initial_value
        self.interest = interest
        self.is_reinvesting_profits = is_reinvesting_profits
        self.successful_cycles = 0
        self.market_timestamp = 0
        self.account_bid_price = 0
        self.market_bid_price = 0
        self.account_ask_price = 0
        self.market_ask_price = 0

    def get_initial_value(self):
        return self.initial_value

    def get_net_profit(self):
        if self.is_reinvesting_profits:
            growth = math.pow(self.interest, self.successful_cycles)
        else:
            growth = self.interest
        return self.initial_value * (growth - 1)

    def get_percent_profit(self):
        return self.get_net_profit() / self.initial_value

    def get_successful_cycles(self):
        return self.successful_cycles

    def set_successful_cycles(self):
        self.successful_cycles += 1

    def get_interest(self):
        return self.interest

    def get_market_bid_price(self):
        return self.market_bid_price

    def set_market_bid_price(self, market_bid_price):
        self.market_bid_price = market_bid_price

    def get_market_ask_price(self):
        return self.market_ask_price

    def set_market_ask_price(self, market_ask_price):
        self.market_ask_price = market_ask_price

    def get_market_timestamp(self):
        return self.market_timestamp

    def set_market_timestamp(self, market_timestamp):
        self.market_timestamp = market_timestamp

    def get_account_ask_price(self):
        return self.account_ask_price

    def set_account_ask_price(self, account_ask_price):
        self.account_ask_price = account_ask_price

    def get_account_bid_price(self):
        return self.account_bid_price

    def set_account_bid_price(self, account_bid_price):
        self.account_bid_price = account_bid_price
