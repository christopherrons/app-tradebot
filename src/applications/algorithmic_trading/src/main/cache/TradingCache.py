import redis


class TradingCache:
    def __init__(self):
        self.__connection = redis.StrictRedis(host='redis', port=6379, db=0, charset="utf-8", decode_responses=True)

    @property
    def initial_value(self) -> float:
        return float(self.__connection.get("initial_value"))

    @initial_value.setter
    def initial_value(self, initial_value: float):
        self.__connection.set("initial_value", initial_value)

    @property
    def cash_value(self) -> float:
        return float(self.__connection.get("cash_value"))

    @cash_value.setter
    def cash_value(self, cash_value: float):
        self.__connection.set("cash_value", cash_value)

    @property
    def gross_position_value(self) -> float:
        return float(self.market_bid_price * self.sell_quantity)

    @property
    def net_position_value(self) -> float:
        return float(self.gross_position_value * (1 - self.exchange_fee))

    @property
    def buy_quantity(self) -> float:
        return float((self.cash_value * (1 - self.exchange_fee)) / self.account_bid_price)

    @property
    def sell_quantity(self) -> float:
        return float(self.__connection.get("sell_quantity"))

    @sell_quantity.setter
    def sell_quantity(self, sell_quantity: float):
        self.__connection.set("sell_quantity", sell_quantity)

    @property
    def successful_cycles(self) -> int:
        return int(self.__connection.get("successful_cycles"))

    @successful_cycles.setter
    def successful_cycles(self, successful_cycles: int):
        self.__connection.set("successful_cycles", successful_cycles)

    @property
    def successful_trades(self) -> int:
        return int(self.__connection.get("successful_trades"))

    @successful_trades.setter
    def successful_trades(self, successful_trades: int):
        self.__connection.set("successful_trades", successful_trades)

    @property
    def interest(self) -> float:
        return float(self.__connection.get("interest"))

    @interest.setter
    def interest(self, interest: float):
        self.__connection.set("interest", interest)

    @property
    def market_bid_price(self) -> float:
        return float(self.__connection.get("market_bid_price"))

    @market_bid_price.setter
    def market_bid_price(self, market_bid_price: float):
        self.__connection.set("market_bid_price", market_bid_price)

    @property
    def market_ask_price(self) -> float:
        return float(self.__connection.get("market_ask_price"))

    @market_ask_price.setter
    def market_ask_price(self, market_ask_price: float):
        self.__connection.set("market_ask_price", market_ask_price)

    @property
    def account_ask_price(self) -> float:
        return float(self.__connection.get("account_ask_price"))

    @account_ask_price.setter
    def account_ask_price(self, account_ask_price: float):
        self.__connection.set("account_ask_price", account_ask_price)

    @property
    def account_bid_price(self) -> float:
        return float(self.__connection.get("account_bid_price"))

    @account_bid_price.setter
    def account_bid_price(self, account_bid_price: float):
        self.__connection.set("account_bid_price", account_bid_price)

    @property
    def accrued_fee(self) -> float:
        return float(self.__connection.get("accrued_fee")) if self.__connection.exists("accrued_fee") else 0

    @accrued_fee.setter
    def accrued_fee(self, fee: float):
        self.__connection.set("accrued_fee", self.accrued_fee + fee)

    @property
    def exchange_fee(self) -> float:
        return float(self.__connection.get("exchange_fee"))

    @exchange_fee.setter
    def exchange_fee(self, exchange_fee: float):
        self.__connection.set("exchange_fee", exchange_fee)


trading_cache = TradingCache()
