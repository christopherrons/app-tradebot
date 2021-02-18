from TradeBot import TradeBot
from Utils.TradeBotUtils import TradeBotUtils
from datetime import datetime, timedelta
from LiveCache import LiveCache


class LiveTradeBot(TradeBot):

    def __init__(self,
                 account_bid_price,
                 interest,
                 initial_value,
                 bitstamp_api,
                 bitstamp_websocket,
                 run_time_minutes,
                 is_reinvesting_profits,
                 print_interval,
                 is_buy=True):

        super().__init__(bitstamp_websocket,
                         LiveCache(initial_value, interest, account_bid_price, is_reinvesting_profits),
                         is_buy)

        self.__bitstamp_api = bitstamp_api
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
        buy_action_id = self.__bitstamp_api.buy_action(self._trade_bot_cache.market_ask_price,
                                                       self._trade_bot_cache.buy_quantity)
        while not self.is_order_status_finished(buy_action_id):
            # TODO add logic for printing while waiting
            pass
        fee = self.__bitstamp_api.get_transaction_fee()
        self._trade_bot_cache.accrued_fee = fee
        self._trade_bot_output.print_and_log_successful_trades(self._is_buy, fee)
        self._is_buy = False
        self.update_account_quantity_values_and_fees()
        self.update_account_prices()
        self._trade_bot_output.send_email()

    def trade_action_sell(self):
        sell_order_id = self.__bitstamp_api.sell_action(self._trade_bot_cache.market_bid_price,
                                                        self._trade_bot_cache.sell_quantity)
        while not self.is_order_status_finished(sell_order_id):
            # TODO add logic for printing while waiting
            pass
        self._trade_bot_cache.increment_successful_cycles()
        fee = self.__bitstamp_api.get_transaction_fee()
        self._trade_bot_cache.accrued_fee = fee
        self._trade_bot_output.print_and_log_successful_trades(self._is_buy)
        self._is_buy = True
        self.update_account_quantity_values_and_fees()
        self.update_account_prices()
        self._trade_bot_output.send_email()

    def update_account_quantity_values_and_fees(self):
        self._trade_bot_cache.sell_quantity = self.__bitstamp_api.get_account_quantity()
        self._trade_bot_cache.cash_value = self.__bitstamp_api.get_account_cash_value()
        #  if self._is_buy:
        #     self._trade_bot_cache.fee = self._bitstamp_api.get_usdxrp_fee()
        # else:
        #   self._trade_bot_cache.fee = self._bitstamp_api.get_xrpusd_fee()

    def is_order_status_finished(self, order_id):
        return self._bitstamp_api.get_order_status(order_id) == "Finished"
