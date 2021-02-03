from TradeBotCache import TradeBotCache
from TradeBotOutput import TradeBotOutput


class CryptoTradeBot:

    def __init__(self, bid_price, interest, initial_value, run_time_minutes, is_reinvesting_profits, is_simulation, is_buy=True):
        self.bid_price = bid_price
        self.run_time_minutes = run_time_minutes
        self.initial_value = initial_value
        self.is_simulation = is_simulation
        self.is_buy = is_buy
        self.ask_price = (1 + interest) * bid_price

        self.trade_bot_cache = TradeBotCache(initial_value, interest, is_reinvesting_profits)
        self.trade_bot_output = TradeBotOutput(self.trade_bot_cache)

    def run(self):
        "Runner"
        while True:
            self.trade_decision_algorithm()
            ## here we shiould print some market data from time to time

    def get_ask_price(self):
        "Gets the current ask price of the crypto currency"
        self.trade_bot_cache.set_market_ask_price()

    def get_bid_price(self):
        "Gets the current bid price of the crypto currency"
        self.trade_bot_cache.set_market_bid_price()

    def trade_decision_algorithm(self):
        "Decision to buy or sell"
        if self.is_buy:
            if self.bid_price >= self.get_ask_price():  # Make sure we dont buy to low e.g buy price = 100 and  ask price = 500.
                self.trade_action_buy()                 # If the price goes below the initial buy price the by some delta then we should adjust the buy and sell price
        else:
            if self.ask_price == self.get_bid_price():
                self.trade_action_sell()

    def trade_action_buy(self):
        "Http-request to Bistamp API"
        if not self.is_simulation:
            if self.is_successful_trade():
                self.trade_bot_cache.set_account_ask_price(self.ask_price)
        self.is_buy = False

    def trade_action_sell(self):
        "Http-request to Bistamp API"
        if not self.is_simulation:
            if self.is_successful_trade():
                self.trade_bot_cache.set_account_bid_price(self.bid_price)
        self.is_buy = True

        self.trade_bot_cache.set_successful_cycles()

    def is_successful_trade(self):
        "checks if the trades has gone through"
        pass
