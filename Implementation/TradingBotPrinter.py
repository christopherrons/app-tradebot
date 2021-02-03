from pip.commands.list import tabulate
from tabulate import tabulate


class TradingBotPrinter:

    def __init__(self, tradingBotCache):
        self.tradingBotCache = tradingBotCache

    def print_market_data(self):
        print(tabulate([[self.tradingBotCache.get_market_timestamp(), self.tradingBotCache.get_market_bid_price(),
                         self.tradingBotCache.get_market_ask_price()]],
                       headers=['Timestamp', 'Bid Price [$]', 'Ask Price [$]']))

    def print_cycle_data(self):
        print(tabulate([[self.tradingBotCache.get_market_timestamp(), bid_price, ask_price]],
                       headers=['Time Stamp', 'Nr Successfully cycles', 'Net Profit [$]', 'Percent Profit [%%]',
                                'Initial Value [$]', 'Interest [%%]']))
