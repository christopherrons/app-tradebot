import time
from datetime import datetime, timedelta

import websockets

from applications.algorithmic_trading.src.main.tradebots.volatilitybots.VolatilityTradeBotBuyer import \
    VolatilityTradeBotBuyer
from applications.algorithmic_trading.src.main.tradebots.volatilitybots.VolatilityTradeBotSeller import \
    VolatilityTradeBotSeller
from applications.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils
from applications.common.src.main.utils.PrinterUtils import PrinterUtils


class VolatilityTradeRunner:

    def __init__(self,
                 is_sell: bool,
                 trade_bot_buyer: VolatilityTradeBotBuyer,
                 trade_bot_seller: VolatilityTradeBotSeller,
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
        PrinterUtils.console_log(message=f"Started trading at {start_time} and will ended at {self.__run_stop_time}")

        delta_minutes = start_time
        while not TradeBotUtils.is_run_time_passed(current_time=datetime.now(), run_stop_time=self.__run_stop_time):

            delta_minutes = self.__print_trading_data(delta_minutes)

            try:
                if self.__trade_bot.is_account_order_matching_market_order():
                    order_id = self.__trade_bot.execute_order()
                    if self.__trade_bot.is_order_executed(order_id):
                        self.__trade_bot.run_post_trade_tasks(order_id)
                        self.__switch_trader()
            except websockets.exceptions.ConnectionClosedError:
                PrinterUtils.console_log(message=f"{datetime.now()}: Attempting to Reconnect Websocket")
                time.sleep(10)
                self.__trade_bot.reconnect_websocket()

        PrinterUtils.console_log(message=f"Started trading at {start_time} and ended at {datetime.now()}")

    def __switch_trader(self):
        if self.__trade_bot == self.__trade_bot_buyer:
            self.__trade_bot = self.__trade_bot_seller
        else:
            self.__trade_bot = self.__trade_bot_buyer

    def __print_trading_data(self, delta_minutes: datetime):
        if (datetime.now() - delta_minutes).seconds >= (self.__print_interval * 60):
            self.__trade_bot.print_trading_data(self.__trade_bot.is_buy())
            return datetime.now()
        return delta_minutes
