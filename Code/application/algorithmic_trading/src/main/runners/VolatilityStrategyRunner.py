from datetime import datetime, timedelta

from services.algorithmic_trading.src.main.tradebots.TradeBotBuyer import TradeBotBuyer
from services.algorithmic_trading.src.main.tradebots.TradeBotSeller import TradeBotSeller
from services.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils


class VolatilityStrategyRunner:

    def __init__(self,
                 is_sell: bool,
                 trade_bot_buyer: TradeBotBuyer,
                 trade_bot_seller: TradeBotSeller,
                 run_time_minutes: float,
                 print_interval: float):

        self.__trade_bot_buyer = trade_bot_buyer
        self.__trade_bot_seller = trade_bot_seller

        if is_sell:
            self.__trade_bot = trade_bot_seller
        else:
            self.__trade_bot = trade_bot_buyer

        self.__run_time_minutes = run_time_minutes
        self.__print_interval = print_interval
        self.__run_stop_time = datetime.now() + timedelta(seconds=(run_time_minutes * 60))

    def run(self):
        start_time = datetime.now()
        print(f"Started trading at {start_time} and will ended at {self.__run_stop_time}\n")

        delta_minutes = start_time
        while not TradeBotUtils.is_run_time_passed(current_time=datetime.now(), run_stop_time=self.__run_stop_time):
            if (datetime.now() - delta_minutes).seconds >= (self.__print_interval * 60):
                self.__trade_bot.print_trading_formation(self.__trade_bot.is_buy())
                delta_minutes = datetime.now()

            if self.__trade_bot.is_trade_able():
                order_id = self.__trade_bot.create_trade()
                if self.__trade_bot.is_trade_successful(order_id):
                    self.__trade_bot.update_cache(order_id)
                    self.__trade_bot.send_email_with_successful_trade()
                    self.__switch_trader()

        print(f"Started trading at {start_time} and ended at {datetime.now()}")

    def __switch_trader(self):
        if self.__trade_bot == self.__trade_bot_buyer:
            self.__trade_bot = self.__trade_bot_seller
        else:
            self.__trade_bot = self.__trade_bot_buyer
