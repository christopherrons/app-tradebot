class TradeBotCache:

    def __init__(self, initial_value: float,
                 cash_value: float,
                 interest: float,
                 account_bid_price: float,
                 account_ask_price: float,
                 sell_quantity: float,
                 exchange_fee: float,
                 accrued_fees: float,
                 success_ful_trades: int,
                 successful_cycles: int):
        self.__initial_value = initial_value
        self.__cash_value = cash_value
        self.__interest = interest
        self.__account_bid_price = account_bid_price
        self.__account_ask_price = account_ask_price
        self.__sell_quantity = sell_quantity
        self.__exchange_fee = exchange_fee
        self.__accrued_fee = accrued_fees
        self.__successful_trades = success_ful_trades
        self.__successful_cycles = successful_cycles
        self.__gross_position_value = 0
        self.__net_position_value = 0
        self.__buy_quantity = 0
        self.__market_bid_price = 0
        self.__market_ask_price = 0

    @property
    def initial_value(self) -> float:
        return self.__initial_value

    @property
    def cash_value(self) -> float:
        return self.__cash_value

    @cash_value.setter
    def cash_value(self, cash_value: float):
        self.__cash_value = cash_value

    @property
    def gross_position_value(self) -> float:
        return self.__market_bid_price * self.__sell_quantity

    @gross_position_value.setter
    def gross_position_value(self, gross_position_value: float):
        self.__gross_position_value = gross_position_value

    @property
    def net_position_value(self) -> float:
        return self.gross_position_value * (1 - self.__exchange_fee)

    @net_position_value.setter
    def net_position_value(self, net_position_value: float):
        self.__net_position_value = net_position_value

    @property
    def buy_quantity(self) -> float:
        return (self.__cash_value * (1 - self.__exchange_fee)) / self.account_bid_price

    @buy_quantity.setter
    def buy_quantity(self, buy_quantity: float):
        self.__buy_quantity = buy_quantity

    @property
    def sell_quantity(self) -> float:
        return self.__sell_quantity

    @sell_quantity.setter
    def sell_quantity(self, sell_quantity: float):
        self.__sell_quantity = sell_quantity

    @property
    def successful_cycles(self) -> int:
        return self.__successful_cycles

    def increment_successful_cycles(self):
        self.__successful_cycles += 1

    @property
    def successful_trades(self) -> int:
        return self.__successful_trades

    def increment_successful_trades(self):
        self.__successful_trades += 1

    @property
    def interest(self) -> float:
        return self.__interest

    @property
    def market_bid_price(self) -> float:
        return self.__market_bid_price

    @market_bid_price.setter
    def market_bid_price(self, market_bid_price: float):
        self.__market_bid_price = market_bid_price

    @property
    def market_ask_price(self) -> float:
        return self.__market_ask_price

    @market_ask_price.setter
    def market_ask_price(self, market_ask_price):
        self.__market_ask_price = market_ask_price

    @property
    def account_ask_price(self) -> float:
        return self.__account_ask_price

    @account_ask_price.setter
    def account_ask_price(self, account_ask_price: float):
        self.__account_ask_price = account_ask_price

    @property
    def account_bid_price(self) -> float:
        return self.__account_bid_price

    @account_bid_price.setter
    def account_bid_price(self, account_bid_price: float):
        self.__account_bid_price = account_bid_price

    @property
    def accrued_fee(self) -> float:
        return self.__accrued_fee

    @accrued_fee.setter
    def accrued_fee(self, fee: float):
        self.__accrued_fee += fee

    @property
    def exchange_fee(self) -> float:
        return self.__exchange_fee

    @exchange_fee.setter
    def exchange_fee(self, exchange_fee: float):
        self.__exchange_fee = exchange_fee
