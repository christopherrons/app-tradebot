from TradeBot import TradeBot
from Utils.TradeBotUtils import TradeBotUtils
from datetime import datetime, timedelta
from SimulationCache import SimulationCache


class SimulationTradeBot(TradeBot):

    def __init__(self,
                 account_bid_price,
                 interest,
                 initial_value,
                 bitstamp_websocket,
                 run_time_minutes,
                 is_reinvesting_profits,
                 print_interval,
                 is_buy=True):

        super().__init__(bitstamp_websocket,
                         SimulationCache(initial_value, interest, account_bid_price, is_reinvesting_profits),
                         is_buy)

        self.__run_stop_time = datetime.now() + timedelta(seconds=(run_time_minutes * 60))
        self.__print_interval = print_interval

    def run(self):
        start_time = datetime.now()
        print(f"Started trading at {start_time} and will ended at {self.__run_stop_time}\n")

        delta_minutes = start_time
        while not TradeBotUtils.is_run_time_passed(datetime.now(), self.__run_stop_time):

            if (datetime.now() - delta_minutes).seconds >= (self.__print_interval * 60):
                self._trade_bot_output.print_and_log_current_formation(self._is_buy)
                delta_minutes = datetime.now()

            if self.is_trade_able():
                self.trade_decision_algorithm()

        print(f"Started trading at {start_time} and ended at {datetime.now()}")

    def trade_decision_algorithm(self):
        if self._is_buy:
            self.trade_action_buy()
        else:
            self.trade_action_sell()

    def trade_action_buy(self):
        self._trade_bot_cache.accrued_fee = self._trade_bot_cache.buy_fee()
        self._trade_bot_output.print_and_log_successful_trades(self._is_buy, self._trade_bot_cache.buy_fee())
        self._is_buy = False
        self._trade_bot_cache.sell_quantity = self._trade_bot_cache.buy_quantity
        self.update_account_prices()
        self.update_position_or_cash_value()
        self._trade_bot_output.send_email()

    def trade_action_sell(self):
        self._trade_bot_cache.increment_successful_cycles()
        self._trade_bot_cache.accrued_fee = self._trade_bot_cache.sell_fee()
        self._trade_bot_output.print_and_log_successful_trades(self._is_buy, self._trade_bot_cache.sell_fee())
        self._is_buy = True
        self.update_account_prices()
        self.update_position_or_cash_value()
        self._trade_bot_output.send_email()

    def update_position_or_cash_value(self):
        if self._is_buy:
            self._trade_bot_cache.position_value = 0
            self._trade_bot_cache.cash_value = self._trade_bot_cache.position_value - self._trade_bot_cache.sell_fee
        else:
            self._trade_bot_cache.cash_value = 0
