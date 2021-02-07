from TradeBot import TradeBot
from TradebotUtils import TradeBotUtils
from datetime import datetime, timedelta
from LiveCache import LiveCache


class LiveTradeBot(TradeBot):

    def __init__(self,
                 account_bid_price,
                 interest,
                 initial_value,
                 bitstamp_token,
                 market,
                 run_time_minutes,
                 is_reinvesting_profits,
                 print_interval,
                 is_reset_logs,
                 is_buy=True):

        super().__init__(bitstamp_token, market, is_reset_logs,
                         LiveCache(initial_value, interest, account_bid_price, is_reinvesting_profits),
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
            self.trade_action_buy()  # If the price goes below the initial buy price the by some delta then we should adjust the buy and sell price
        else:
            self.trade_action_sell()

    def trade_action_buy(self):
        "Http-request to Bistamp API"
        # THe buy price is taken from the market_ask_price in the cache
        if self.is_successful_trade():
            trade_value = self._trade_bot_cache.market_ask_price  # need the quantity aswell
            self._trade_bot_output.print_and_log_successful_trades(self._is_buy, -trade_value)
            self._is_buy = False
            self.update_account_prices()
            self.update_position_or_cash_value()

    def trade_action_sell(self):
        "Http-request to Bistamp API"
        # THe sell price is taken from the market_bid_price in the cache
        if self.is_successful_trade():
            trade_value = self._trade_bot_cache.market_bid_price  # need quantity
            self._trade_bot_output.print_and_log_successful_trades(self._is_buy, trade_value)
            self._is_buy = True
            self._trade_bot_cache.increment_successful_cycles()
            self.update_account_prices()
            self.update_position_or_cash_value()

    def is_successful_trade(self):
        "checks if the trades has gone through"
        pass

    def update_position_or_cash_value(self):
        if self._is_buy:
            self._trade_bot_cache.position_value = 0
            self._trade_bot_cache.position_value = self._trade_bot_cache.market_bid_price  # not exactly true, need to check the value of the trade
        else:
            self._trade_bot_cache.cash_value = 0
            self._trade_bot_cache.position_value = self._trade_bot_cache.market_ask_price  # not exactly true, need to check the value of the trade
