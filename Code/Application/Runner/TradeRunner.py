from datetime import datetime, timedelta

from Services.Runner.Utils.TradeBotUtils import TradeBotUtils


class TradeRunner:

    def __init__(self,
                 is_buy,
                 trade_bot_buyer,
                 trade_bot_seller,
                 run_time_minutes,
                 print_interval):

        self.__trade_bot_buyer = trade_bot_buyer
        self.__trade_bot_seller = trade_bot_seller

        if is_buy:
            self.__trade_bot = trade_bot_buyer
        else:
            self.__trade_bot = trade_bot_seller

        self.__run_time_minutes = run_time_minutes
        self.__print_interval = print_interval
        self.__run_stop_time = datetime.now() + timedelta(seconds=(run_time_minutes * 60))

    def run(self):
        start_time = datetime.now()
        print(f"Started trading at {start_time} and will ended at {self.__run_stop_time}\n")

        delta_minutes = start_time
        while not TradeBotUtils.is_run_time_passed(datetime.now(), self.__run_stop_time):

            if (datetime.now() - delta_minutes).seconds >= (self.__print_interval * 60):
                self.__trade_bot.print_and_log_current_formation(self.__trade_bot.is_buy())
                delta_minutes = datetime.now()

            if self.__trade_bot.is_trade_able():
                if self.__trade_bot.create_trade():
                    self.switch_trader()

        print(f"Started trading at {start_time} and ended at {datetime.now()}")

    def switch_trader(self):
        if self.__trade_bot == self.__trade_bot_buyer:
            self.__trade_bot = self.__trade_bot_seller
        else:
            self.__trade_bot = self.__trade_bot_buyer
