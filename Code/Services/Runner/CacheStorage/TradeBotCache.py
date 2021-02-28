class TradeBotCache:

    def __init__(self, initial_value,
                 cash_value,
                 interest,
                 account_bid_price,
                 account_ask_price,
                 sell_quantity,
                 exchange_fee):
        self.__initial_value = initial_value
        self.__cash_value = cash_value
        self.__interest = interest
        self.__account_bid_price = account_bid_price
        self.__account_ask_price = account_ask_price
        self.__sell_quantity = sell_quantity
        self.__exchange_fee = exchange_fee
        self.__position_value = 0
        self.__buy_quantity = 0
        self.__successful_trades = 0
        self.__successful_cycles = 0
        self.__market_timestamp = 0
        self._market_bid_price = 0
        self._market_ask_price = 0
        self.__accrued_fee = 0

    @property
    def initial_value(self):
        return self.__initial_value

    @property
    def cash_value(self):
        return self.__cash_value

    @cash_value.setter
    def cash_value(self, cash_value):
        self.__cash_value = cash_value

    @property
    def position_value(self):
        return self._market_bid_price * self.__sell_quantity

    @position_value.setter
    def position_value(self, position_value):
        self.__position_value = position_value

    @property
    def buy_quantity(self):
        return (self.__cash_value * (1 - self.__exchange_fee)) / self.account_bid_price

    @buy_quantity.setter
    def buy_quantity(self, buy_quantity):
        self.__buy_quantity = buy_quantity

    @property
    def sell_quantity(self):
        return self.__sell_quantity

    @sell_quantity.setter
    def sell_quantity(self, sell_quantity):
        self.__sell_quantity = sell_quantity

    @property
    def successful_cycles(self):
        return self.__successful_cycles

    def increment_successful_cycles(self):
        self.__successful_cycles += 1

    @property
    def successful_trades(self):
        return self.__successful_trades

    def increment_successful_trades(self):
        self.__successful_trades += 1

    @property
    def interest(self):
        return self.__interest

    @property
    def market_bid_price(self):
        return self._market_bid_price

    @market_bid_price.setter
    def market_bid_price(self, market_bid_price):
        self._market_bid_price = market_bid_price

    @property
    def market_ask_price(self):
        return self._market_ask_price

    @market_ask_price.setter
    def market_ask_price(self, market_ask_price):
        self._market_ask_price = market_ask_price

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

    @property
    def accrued_fee(self):
        return self.__accrued_fee

    @accrued_fee.setter
    def accrued_fee(self, fee):
        self.__accrued_fee += fee

    @property
    def exchange_fee(self):
        return self.__exchange_fee

    @exchange_fee.setter
    def exchange_fee(self, exchange_fee):
        self.__exchange_fee = exchange_fee
