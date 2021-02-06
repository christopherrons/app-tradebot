from tabulate import tabulate
import logging

logging.basicConfig(filename="logs/tradeBotLogs.log",
                    filemode="a",
                    level=logging.DEBUG)
logger = logging.getLogger()


class TradeBotOutput:

    def __init__(self, trade_bot_cache):
        self.trade_bot_cache = trade_bot_cache

    def print_data(self, is_buy):
        if is_buy:
            account_trade = "Account Bid Price [$]"
            account_trade_price = self.trade_bot_cache.get_account_bid_price()
            market_trade = "Account Ask Price [$]"
            market_trade_price = self.trade_bot_cache.get_market_ask_price()
        else:
            account_trade = "Account Ask Price [$]"
            account_trade_price = self.trade_bot_cache.get_account_ask_price()
            market_trade = "Market Bid Price [$]"
            market_trade_price = self.trade_bot_cache.get_market_bid_price()


        headers = ['Timestamp', account_trade, market_trade, 'Nr Successfully cycles', 'Net Profit [$]',
                   'Percent Profit [%]', 'Initial Value [$]', 'Interest [%]']
        output = [self.trade_bot_cache.get_market_timestamp(), account_trade_price,
                  market_trade_price, self.trade_bot_cache.get_successful_cycles(),
                  self.trade_bot_cache.get_net_profit(), self.trade_bot_cache.get_percent_profit(),
                  self.trade_bot_cache.get_initial_value(), self.trade_bot_cache.get_interest() * 100]

        tabulated_output = tabulate([output], headers=headers)
        print(tabulated_output + "\n")
        logger.info(tabulated_output)
