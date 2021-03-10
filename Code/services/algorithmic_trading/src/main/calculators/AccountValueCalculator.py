import math

from services.algorithmic_trading.src.main.cache_storage.TradeBotCache import TradeBotCache


class AccountValueCalculator:

    def __init__(self, trade_bot_cache: TradeBotCache):
        self.__trade_bot_cache = trade_bot_cache

    def cash_profit(self) -> float:
        return self.__trade_bot_cache.cash_value - self.__trade_bot_cache.initial_value

    def percent_cash_profit(self) -> float:
        return 100 * (self.__trade_bot_cache.cash_value / self.__trade_bot_cache.initial_value - 1)

    def theoretical_cash_profit(self) -> float:
        return math.pow(self.__trade_bot_cache.interest, self.__trade_bot_cache.successful_cycles)

    def theoretical_percent_profit(self) -> float:
        self.theoretical_cash_profit() / self.__trade_bot_cache.initial_value

    def net_position_profit(self) -> float:
        return self.__trade_bot_cache.net_position_value - self.__trade_bot_cache.initial_value

    def percent_position_profit(self) -> float:
        return 100 * (self.__trade_bot_cache.net_position_value / self.__trade_bot_cache.initial_value - 1)
