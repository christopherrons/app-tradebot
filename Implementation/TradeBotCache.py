class TradeBotCache:

    def __init__(self, initial_value, interest, account_bid_price, is_reinvesting_profits):
        self.__initial_value = initial_value
        self.__interest = interest
        self.__account_bid_price = account_bid_price
        self.__account_ask_price = (1 + interest) * account_bid_price
        self.__is_reinvesting_profits = is_reinvesting_profits
        self.__successful_cycles = 0
        self.__market_timestamp = 0
        self.__market_bid_price = 0
        self.__market_ask_price = 0
        self.__position_value = 0
        self.__buy_quantity = 0
        self.__sell_quantity = 0
        self.__cash_value = 0

    @property
    def initial_value(self):
        return self.__initial_value

    @property
    def successful_cycles(self):
        return self.__successful_cycles

    def increment_successful_cycles(self):
        self.__successful_cycles += 1

    @property
    def interest(self):
        return self.__interest

    @property
    def market_bid_price(self):
        return self.__market_bid_price

    @market_bid_price.setter
    def market_bid_price(self, market_bid_price):
        self.__market_bid_price = market_bid_price

    @property
    def market_ask_price(self):
        return self.__market_ask_price

    @market_ask_price.setter
    def market_ask_price(self, market_ask_price):
        self.__market_ask_price = market_ask_price

    @property
    def market_timestamp(self):
        return self.__market_timestamp

    @market_timestamp.setter
    def market_timestamp(self, market_timestamp):
        self.__market_timestamp = market_timestamp

    @property
    def account_ask_price(self):
        return self.__account_ask_price

    @account_ask_price.setter
    def account_ask_price(self, account_ask_price):
        self.__account_ask_price = account_ask_price

    @property
    def account_bid_price(self):
        return self.__account_bid_price

    @account_bid_price.setter
    def account_bid_price(self, account_bid_price):
        self.__account_bid_price = account_bid_price