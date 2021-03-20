import math


class ProfitCalculatorUtil:

    @staticmethod
    def cash_profit(cash_value: float, initial_value: float) -> float:
        return cash_value - initial_value

    @staticmethod
    def percent_cash_profit(cash_value: float, initial_value: float) -> float:
        return 100 * (cash_value / initial_value - 1)

    @staticmethod
    def theoretical_cash_profit(initial_value: float, net_interest: float, successful_cycles: int) -> float:
        return initial_value * (math.pow(net_interest, successful_cycles) - 1)

    @staticmethod
    def theoretical_percent_profit(initial_value: float, net_interest: float, successful_cycles: int) -> float:
        return ProfitCalculatorUtil.theoretical_cash_profit(initial_value, net_interest, successful_cycles) / initial_value

    @staticmethod
    def net_position_profit(net_position_value: float, initial_value: float) -> float:
        return net_position_value - initial_value

    @staticmethod
    def percent_position_profit(net_position_value: float, initial_value: float) -> float:
        return 100 * (net_position_value / initial_value - 1)
