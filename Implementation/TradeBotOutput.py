from tabulate import tabulate
import logging

logging.basicConfig(filename="../logs/tradeBotLogs.log",
                    filemode="a",
                    level=logging.DEBUG)
logger = logging.getLogger()


# We should add logging to this class so we can check the files
class TradeBotOutput:

    def __init__(self, trade_bot_cache):
        self.trade_bot_ache = trade_bot_cache

    def print_market_data(self):
        headers = ['Timestamp', 'Account Bid Price', 'Market Bid Price [$]', 'Account Ask Price',
                   'Market Ask Price [$]']
        output = [self.trade_bot_ache.get_market_timestamp(), self.trade_bot_ache.get_account_bid_price(),
                  self.trade_bot_ache.get_market_bid_price(), self.trade_bot_ache.get_account_ask_price(),
                  self.trade_bot_ache.get_market_ask_price()]
        tabulated_output = tabulate([output], headers=headers)
        print(tabulated_output)
        logger.info(tabulated_output)

    def print_cycle_data(self):
        headers = ['Time Stamp', 'Nr Successfully cycles', 'Net Profit [$]', 'Percent Profit [%%]',
                   'Initial Value [$]', 'Interest [%%]']
        output = [self.trade_bot_ache.get_market_timestamp(), self.trade_bot_ache.get_successful_cycles(),
                  self.trade_bot_ache.get_net_profit(), self.trade_bot_ache.get_percent_profit(),
                  self.trade_bot_ache.get_interest(), ]
        tabulated_output = tabulate([output], headers=headers)
        print(tabulated_output)
        logger.info(tabulated_output)
