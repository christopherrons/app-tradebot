import math


class Calculator:

    def __init__(self, trade_bot_cache):
        self.__trade_bot_cache = trade_bot_cache

    def gross_cash_profit(self):
        return self.__trade_bot_cache.cash_value - self.__trade_bot_cache.initial_value

    def percent_cash_profit(self):
        return 100 * (self.__trade_bot_cache.cash_value / self.__trade_bot_cache.initial_value - 1)

    def theoretical_cash_profit(self):
        if self.__trade_bot_cache.__is_reinvesting_profits:
            growth = math.pow(self.__trade_bot_cache.interest, self.__trade_bot_cache.successful_cycles)
        else:
            growth = self.__trade_bot_cache.interest
        return self.__trade_bot_cache.initial_value * (growth - 1)

    def theoretical_percent_profit(self):
        self.theoretical_cash_profit() / self.__trade_bot_cache.initial_value

    def gross_position_profit(self):
        return self.__trade_bot_cache.position_value - self.__trade_bot_cache.initial_value

    def percent_position_profit(self):
        return 100 * (self.__trade_bot_cache.position_value / self.__trade_bot_cache.initial_value - 1)
