from datetime import datetime, timedelta

from services.algorithmic_trading.src.main.tradebots.volatilitybots.VolatilityTradeBotBuyer import \
    VolatilityTradeBotBuyer
from services.algorithmic_trading.src.main.tradebots.volatilitybots.VolatilityTradeBotSeller import \
    VolatilityTradeBotSeller
from services.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils


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
        print(f"Started trading at {start_time} and will ended at {self.__run_stop_time}\n")

        delta_minutes = start_time
        while not TradeBotUtils.is_run_time_passed(current_time=datetime.now(), run_stop_time=self.__run_stop_time):
            if (datetime.now() - delta_minutes).seconds >= (self.__print_interval * 60):
                self.__trade_bot.print_trading_formation(self.__trade_bot.is_buy())
                delta_minutes = datetime.now()

            if self.__trade_bot.is_account_price_matching_market_price():
                order_id = self.__trade_bot.execute_order()
                if self.__trade_bot.is_order_executed(order_id):
                    self.__trade_bot.run_post_trade_batch(order_id)
                    self.__switch_trader()

        print(f"Started trading at {start_time} and ended at {datetime.now()}")

    def __switch_trader(self):
        if self.__trade_bot == self.__trade_bot_buyer:
            self.__trade_bot = self.__trade_bot_seller
        else:
            self.__trade_bot = self.__trade_bot_buyer
