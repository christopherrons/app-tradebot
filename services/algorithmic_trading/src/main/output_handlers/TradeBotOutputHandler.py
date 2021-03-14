from datetime import datetime

from services.algorithmic_trading.src.main.cache_storage.TradeBotCache import TradeBotCache
from services.algorithmic_trading.src.main.calculators.ProfitCalculatorUtil import ProfitCalculatorUtil
from services.algorithmic_trading.src.main.database.DatabaseService import DatabaseService
from services.algorithmic_trading.src.main.output_handlers.EmailHandler import EmailHandler
from services.algorithmic_trading.src.main.output_handlers.PlotHandler import PlotHandler
from services.algorithmic_trading.src.main.output_handlers.utils.PrinterUtils import PrinterUtils
from services.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils


class TradeBotOutputHandler:

    def __init__(self, exchange_name: str,
                 trade_bot_cache: TradeBotCache,
                 database_service: DatabaseService,
                 cash_currency: str,
                 crypto_currency: str):
        self.__exchange_name = exchange_name
        self.__trade_bot_cache = trade_bot_cache
        self.__database_service = database_service
        self.__cash_currency = cash_currency
        self.__crypto_currency = crypto_currency

        self.__email_handler = EmailHandler()
        self.__plot_handler = PlotHandler(trade_bot_cache.initial_value, trade_bot_cache.interest, exchange_name,
                                          cash_currency, crypto_currency)
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
            percent_profit_value = ProfitCalculatorUtil.percent_cash_profit(cash_value=current_value,
                                                                            initial_value=self.__trade_bot_cache.initial_value)

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
            percent_profit_value = ProfitCalculatorUtil.percent_cash_profit(cash_value=current_value,
                                                                            initial_value=self.__trade_bot_cache.initial_value)

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
        PrinterUtils.log_data(headers=headers, output=output,
                              file_path=TradeBotUtils.get_information_log_path(self.__exchange_name))

    def print_and_store_trade_report(self, is_buy: bool, fee: float):
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
        PrinterUtils.log_data(headers=headers, output=output,
                              file_path=TradeBotUtils.get_trade_log_path(self.__exchange_name))

        self.__database_service.insert_trade_report(exchange=self.__exchange_name, timestamp=datetime.now(),
                                                    trade_number=self.__trade_bot_cache.successful_trades, buy=is_buy,
                                                    sell=not is_buy, price=price, quantity=quantity,
                                                    cash_currency=self.__cash_currency,
                                                    crypto_currency=self.__crypto_currency,
                                                    gross_trade_value=value, net_trade_value=value - fee, fee=fee)

    def create_visual_trade_report(self):
        self.__plot_handler.create_visual_trade_report()

    def email_trade_reports(self):
        self.__email_handler.send_email_with_attachment(
            email_subject=f"{self.__exchange_name}: Trade Number {self.__trade_bot_cache.successful_trades}",
            email_message=f'Review logs',
            attachment_file_paths=[TradeBotUtils.get_trade_log_path(self.__exchange_name),
                                   TradeBotUtils.get_trade_report_path(self.__exchange_name)])
