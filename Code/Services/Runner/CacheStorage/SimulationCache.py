from Services.Runner.CacheStorage.TradeBotCache import TradeBotCache


class SimulationCache(TradeBotCache):

    def __init__(self, initial_value, interest, account_bid_price, is_reinvesting_profits):
        super().__init__(initial_value, interest, account_bid_price, is_reinvesting_profits)

        self.__cash_value = initial_value
        self.__position_value = 0
        self.__buy_quantity = 0
        self.__sell_quantity = 0

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
        return (self.__cash_value * (1 - self._fee)) / self.account_bid_price

    @buy_quantity.setter
    def buy_quantity(self, buy_quantity):
        self.__buy_quantity = buy_quantity

    @property
    def sell_quantity(self):
        return self.__sell_quantity

    @sell_quantity.setter
    def sell_quantity(self, sell_quantity):
        self.__sell_quantity = sell_quantity

    def buy_fee(self):
        return self.__cash_value * self._fee

    def sell_fee(self):
        return self.position_value * self._fee
