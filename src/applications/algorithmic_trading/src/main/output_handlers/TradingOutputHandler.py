from datetime import datetime

from applications.algorithmic_trading.src.main.cache.TradingCache import trading_cache
from applications.algorithmic_trading.src.main.calculators.ProfitCalculatorUtil import ProfitCalculatorUtil
from applications.algorithmic_trading.src.main.output_handlers.PlotHandler import PlotHandler
from applications.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils
from applications.common.src.main.database import DatabaseService
from applications.common.src.main.email.EmailHandler import EmailHandler
from applications.common.src.main.utils.PrinterUtils import PrinterUtils


class TradingOutputHandler:

    def __init__(self, is_live: bool,
                 exchange_name: str,
                 database_service: DatabaseService,
                 cash_currency: str,
                 crypto_currency: str):
        self.__is_live = is_live
        self.__exchange_name = exchange_name
        self.__database_service = database_service
        self.__cash_currency = cash_currency
        self.__crypto_currency = crypto_currency

        self.__email_handler = EmailHandler()
        self.__plot_handler = PlotHandler(exchange_name, cash_currency, crypto_currency, database_service, is_live, trading_cache.initial_value)
        self.__currency_symbols = TradeBotUtils.get_cash_currency_symbols()

    def print_trading_data(self, is_buy: bool):
        if is_buy:
            account_trade = f"Account Bid Price [{self.__currency_symbols[self.__cash_currency]}]"
            account_trade_price = trading_cache.account_bid_price

            market_trade = f"Market Ask Price [{self.__currency_symbols[self.__cash_currency]}]"
            market_trade_price = trading_cache.market_ask_price

            current_value_description = "Cash Value"
            current_value = trading_cache.cash_value

            trade_quantity = f"Buy Quantity {self.__crypto_currency.upper()}"
            trade_quantity_value = trading_cache.buy_quantity

            percent_profit = "Cash Profit [%]"
            percent_profit_value = ProfitCalculatorUtil.percent_cash_profit(cash_value=current_value,
                                                                            initial_value=trading_cache.initial_value)

        else:
            account_trade = f"Account Ask Price [{self.__currency_symbols[self.__cash_currency]}]"
            account_trade_price = trading_cache.account_ask_price

            market_trade = f"Market Bid Price [{self.__currency_symbols[self.__cash_currency]}]"
            market_trade_price = trading_cache.market_bid_price

            current_value_description = f"Position Net Value [{self.__currency_symbols[self.__cash_currency]}]"
            current_value = trading_cache.net_position_value

            trade_quantity = f"Sell Quantity {self.__crypto_currency.upper()}"
            trade_quantity_value = trading_cache.sell_quantity

            percent_profit = "Position Profit [%]"
            percent_profit_value = ProfitCalculatorUtil.percent_cash_profit(cash_value=current_value,
                                                                            initial_value=trading_cache.initial_value)

        headers = ['Timestamp', trade_quantity, account_trade, market_trade,
                   f'Initial Value [{self.__currency_symbols[self.__cash_currency]}]',
                   current_value_description, percent_profit,
                   f'Accrued Fees [{self.__currency_symbols[self.__cash_currency]}]', 'Nr Buy+Sell Cycles']

        output = [datetime.now(), trade_quantity_value, account_trade_price,
                  market_trade_price, trading_cache.initial_value, current_value,
                  percent_profit_value, trading_cache.accrued_fee, trading_cache.successful_cycles]

        PrinterUtils.print_data_as_tabulate(headers=headers, output=output)

        self.__log_trading_data(is_buy, headers, output)

    def __log_trading_data(self, is_buy: bool, headers: list, output: list):
        headers[1] = "Account Trade Price"
        headers[2] = "Market Trade Price"
        headers.insert(1, "Is Buy")
        output.insert(1, is_buy)
        PrinterUtils.log_data(headers=headers, output=output,
                              file_path=TradeBotUtils.get_generated_file_path(f"{self.__exchange_name.lower()}_trading_data_log.csv"))

    def print_and_store_trade_report(self, is_buy: bool, fee: float, order_id: str):
        if is_buy:
            value = trading_cache.cash_value
            quantity = trading_cache.buy_quantity
            price = trading_cache.market_ask_price
        else:
            value = trading_cache.gross_position_value
            quantity = trading_cache.sell_quantity
            price = trading_cache.market_bid_price

        headers = ['Timestamp', 'is_live', 'exchanges', 'Trade Number', 'Is Buy',
                   f'Price [{self.__currency_symbols[self.__cash_currency]}]',
                   f'Quantity {self.__crypto_currency.upper()}',
                   f'Gross Trade Value [{self.__currency_symbols[self.__cash_currency]}]',
                   f'Net Trade Value [{self.__currency_symbols[self.__cash_currency]}]',
                   f'Fee [{self.__currency_symbols[self.__cash_currency]}]']
        output = [datetime.now(), self.__is_live, self.__exchange_name, trading_cache.successful_trades, is_buy, price, quantity,
                  value, value - fee, fee]

        PrinterUtils.print_data_as_tabulate(headers, output)
        PrinterUtils.log_data(headers=headers, output=output,
                              file_path=TradeBotUtils.get_generated_file_path(f"{self.__exchange_name.lower()}_successful_trade_log.csv"))

        self.__database_service.insert_trade_report(order_id=order_id, is_live=self.__is_live, exchange=self.__exchange_name,
                                                    trade_number=trading_cache.successful_trades,
                                                    timestamp=datetime.now(), buy=is_buy, price=price, quantity=quantity,
                                                    cash_currency=self.__cash_currency, crypto_currency=self.__crypto_currency,
                                                    gross_trade_value=value, net_trade_value=value - fee, fee=fee)

    def create_visual_trade_report(self):
        self.__plot_handler.create_visual_trade_report()

    def email_trade_reports(self):
        self.__email_handler.send_email_with_attachment(
            email_subject=f"{self.__exchange_name}: Trade Number {trading_cache.successful_trades}",
            email_message=f'Review logs',
            attachment_file_paths=[TradeBotUtils.get_generated_file_path(f"{self.__exchange_name.lower()}_successful_trade_log.csv"),
                                   TradeBotUtils.get_generated_file_path(f"{self.__exchange_name.lower()}_trade_report.html")])
