from datetime import datetime

from services.algorithmic_trading.src.main.cache_storage.TradeBotCache import TradeBotCache
from services.algorithmic_trading.src.main.calculators.AccountValueCalculator import AccountValueCalculator
from services.algorithmic_trading.src.main.output_handlers.EmailHandler import EmailHandler
from services.algorithmic_trading.src.main.output_handlers.utils.PrinterUtils import PrinterUtils
from services.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils


class TradeBotOutputHandler:

    def __init__(self, exchange_name: str,
                 trade_bot_cache: TradeBotCache,
                 cash_currency: str,
                 crypto_currency: str):
        self.__cash_currency = cash_currency
        self.__crypto_currency = crypto_currency
        self.__trade_bot_cache = trade_bot_cache
        self.__exchange_name = exchange_name

        self.__email_handler = EmailHandler()
        self.__trading_formation_log_file = TradeBotUtils.get_information_log_path(exchange_name)
        self.__successful_trade_log = TradeBotUtils.get_trade_log_path(exchange_name)
        self.__calculator = AccountValueCalculator(trade_bot_cache)
        self.__currency_symbols = TradeBotUtils.get_cash_currency_symbols()

    def print_trading_formation(self, is_buy: bool):
        if is_buy:
            account_trade = f"Account Bid Price [{self.__currency_symbols[self.__cash_currency]}]"
            account_trade_price = self.__trade_bot_cache.account_bid_price

            market_trade = f"Market Ask Price [{self.__currency_symbols[self.__cash_currency]}]"
            market_trade_price = self.__trade_bot_cache.market_ask_price

            current_value_description = "Cash Value"
            current_value = self.__trade_bot_cache.cash_value

            trade_quantity = f"Buy Quantity {self.__crypto_currency.upper()}"
            trade_quantity_value = self.__trade_bot_cache.buy_quantity

            percent_profit = "Cash Profit [%]"
            percent_profit_value = self.__calculator.percent_cash_profit()

        else:
            account_trade = f"Account Ask Price [{self.__currency_symbols[self.__cash_currency]}]"
            account_trade_price = self.__trade_bot_cache.account_ask_price

            market_trade = f"Market Bid Price [{self.__currency_symbols[self.__cash_currency]}]"
            market_trade_price = self.__trade_bot_cache.market_bid_price

            current_value_description = f"Position Net Value [{self.__currency_symbols[self.__cash_currency]}]"
            current_value = self.__trade_bot_cache.net_position_value

            trade_quantity = f"Sell Quantity {self.__crypto_currency.upper()}"
            trade_quantity_value = self.__trade_bot_cache.sell_quantity

            percent_profit = "Position Profit [%]"
            percent_profit_value = self.__calculator.percent_position_profit()

        headers = ['Timestamp', trade_quantity, account_trade, market_trade,
                   f'Initial Value [{self.__currency_symbols[self.__cash_currency]}]',
                   current_value_description, percent_profit,
                   f'Accrued Fees [{self.__currency_symbols[self.__cash_currency]}]', 'Nr Buy+Sell Cycles']

        output = [datetime.now(), trade_quantity_value, account_trade_price,
                  market_trade_price, self.__trade_bot_cache.initial_value, current_value,
                  percent_profit_value, self.__trade_bot_cache.accrued_fee, self.__trade_bot_cache.successful_cycles]

        PrinterUtils.print_data_as_tabulate(headers=headers, output=output)

        self.__log_trading_information(is_buy, headers, output)

    def __log_trading_information(self, is_buy: bool, headers: list, output: list):
        headers[1] = "Account Trade Price"
        headers[2] = "Market Trade Price"
        headers.insert(1, "Is Buy")
        output.insert(1, is_buy)
        PrinterUtils.log_data(headers=headers, output=output, file_path=self.__trading_formation_log_file)

    def print_successful_trades(self, is_buy: bool, fee: float):
        if is_buy:
            value = self.__trade_bot_cache.cash_value
            quantity = self.__trade_bot_cache.buy_quantity
            price = self.__trade_bot_cache.market_ask_price
        else:
            value = self.__trade_bot_cache.gross_position_value
            quantity = self.__trade_bot_cache.sell_quantity
            price = self.__trade_bot_cache.market_bid_price

        headers = ['Timestamp', 'exchange', 'Trade Number', 'Is Buy',
                   f'Price [{self.__currency_symbols[self.__cash_currency]}]',
                   f'Quantity {self.__crypto_currency.upper()}',
                   f'Gross Trade Value [{self.__currency_symbols[self.__cash_currency]}]',
                   f'Net Trade Value [{self.__currency_symbols[self.__cash_currency]}]',
                   f'Fee [{self.__currency_symbols[self.__cash_currency]}]']
        output = [datetime.now(), self.__exchange_name, self.__trade_bot_cache.successful_trades, is_buy, price,
                  quantity, value, value - fee, fee]

        PrinterUtils.print_data_as_tabulate(headers, output)
        PrinterUtils.log_data(headers=headers, output=output, file_path=self.__successful_trade_log)

    def send_email_with_successful_trade(self):
        self.__email_handler.send_email_with_attachment(
            email_subject=f"{self.__exchange_name}: Trade Number {self.__trade_bot_cache.successful_trades}",
            email_message=f'Review logs',
            attachment_file_paths=[self.__successful_trade_log])
