import csv
import os
import smtplib
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from tabulate import tabulate

from Services.Runner.Calculators.AccountValueCalculator import Calculator
from Services.Runner.Utils.TradeBotUtils import TradeBotUtils


class TradeBotOutput:

    def __init__(self, trade_bot_cache, cash_currency, crypto_currency):
        self.cash_currency = cash_currency
        self.crypto_currency = crypto_currency
        self.__trade_bot_cache = trade_bot_cache
        self.__current_formation_log_file = TradeBotUtils.get_information_log_path()
        self.__successful_trade_log = TradeBotUtils.get_trade_log_path()
        self.__calculator = Calculator(trade_bot_cache)

        self.currency_symbols = {
            'USD': '$',
            'EUR': '€'
        }

    def print_and_log_current_formation(self, is_buy):
        if is_buy:
            account_trade = f"Account Bid Price {self.currency_symbols[self.cash_currency]}"
            account_trade_price = self.__trade_bot_cache.account_bid_price

            market_trade = f"Market Ask Price {self.currency_symbols[self.cash_currency]}"
            market_trade_price = self.__trade_bot_cache.market_ask_price

            current_value_description = "Cash Value"
            current_value = self.__trade_bot_cache.cash_value

            net_profit = f"Cash Profit {self.currency_symbols[self.cash_currency]}"
            net_profit_value = self.__calculator.cash_profit()

            trade_quantity = f"Buy Quantity {self.crypto_currency.upper()}"
            trade_quantity_value = self.__trade_bot_cache.buy_quantity

            percent_profit = "Cash Profit [%]"
            percent_profit_value = self.__calculator.percent_cash_profit()

        else:
            account_trade = f"Account Ask Price {self.currency_symbols[self.cash_currency]}"
            account_trade_price = self.__trade_bot_cache.account_ask_price

            market_trade = f"Market Bid Price {self.currency_symbols[self.cash_currency]}"
            market_trade_price = self.__trade_bot_cache.market_bid_price

            current_value_description = f"Position Net Value {self.currency_symbols[self.cash_currency]}"
            current_value = self.__trade_bot_cache.net_position_value

            net_profit = f"Position Profit {self.currency_symbols[self.cash_currency]}"
            net_profit_value = self.__calculator.net_position_profit()

            trade_quantity = f"Sell Quantity {self.crypto_currency.upper()}"
            trade_quantity_value = self.__trade_bot_cache.sell_quantity

            percent_profit = "Position Profit [%]"
            percent_profit_value = self.__calculator.percent_position_profit()

        headers = ['Timestamp', trade_quantity, account_trade, market_trade,
                   'Initial Value {self.currency_symbols[self.cash_currency]}',
                   current_value_description, percent_profit,
                   f'Accrued Fees {self.currency_symbols[self.cash_currency]}', 'Nr Buy+Sell Cycles']

        output = [datetime.now(), trade_quantity_value, account_trade_price,
                  market_trade_price, self.__trade_bot_cache.initial_value, current_value,
                  percent_profit_value, self.__trade_bot_cache.accrued_fee, self.__trade_bot_cache.successful_cycles]

        self.print_data(headers, output)

        headers[1] = "Account Trade Price"
        headers[2] = "Market Trade Price"
        headers.insert(1, "Is Buy")
        output.insert(1, is_buy)
        self.log_data(headers, output, self.__current_formation_log_file)

    def print_and_log_successful_trades(self, exchange_name, is_buy, fee):
        if is_buy:
            value = self.__trade_bot_cache.cash_value
            quantity = self.__trade_bot_cache.buy_quantity
            price = self.__trade_bot_cache.market_ask_price
        else:
            value = self.__trade_bot_cache.gross_position_value
            quantity = self.__trade_bot_cache.sell_quantity
            price = self.__trade_bot_cache.market_bid_price

        headers = ['Timestamp', 'Exchange', 'Trade Number', 'Is Buy',
                   f'Price {self.currency_symbols[self.cash_currency]}', 'Quantity {self.crypto_currency.upper()}',
                   f'Gross Trade Value {self.currency_symbols[self.cash_currency]}',
                   f'Net Trade Value {self.currency_symbols[self.cash_currency]}',
                   f'Fee {self.currency_symbols[self.cash_currency]}']
        output = [datetime.now(), exchange_name, self.__trade_bot_cache.successful_trades, is_buy, price, quantity,
                  value, value - fee, fee]
        self.print_data(headers, output)
        self.log_data(headers, output, self.__successful_trade_log)

    def print_data(self, headers, output):
        tabulated_output = tabulate([output], headers=headers)
        print(tabulated_output + "\n\n\n\n\n\n")

    def log_data(self, headers, output, file):
        with open(file, 'a+') as f:
            writer = csv.writer(f)
            if os.stat(file).st_size == 0:
                writer.writerow(headers)
                writer.writerow(output)
            else:
                writer.writerow(output)

    def send_email(self, exchange_name):
        email_source = TradeBotUtils.get_email_source()
        email_source_password = TradeBotUtils.get_email_source_password()
        email_target = TradeBotUtils.get_email_target()

        message = MIMEMultipart()
        message['From'] = email_source
        message['To'] = email_target
        message['Subject'] = f"{exchange_name}: Trade Number {self.__trade_bot_cache.successful_trades}"
        message.attach(MIMEText(f'Review logs', 'plain'))

        trade_log = open(self.__successful_trade_log, "rb")
        part_trade = MIMEBase('applications', 'octet-stream')
        part_trade.set_payload(trade_log.read())
        encoders.encode_base64(part_trade)
        part_trade.add_header('Content-Disposition',
                              'attachment; filename=%s' % os.path.basename(self.__successful_trade_log))
        message.attach(part_trade)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        server.login(email_source, email_source_password)
        text = message.as_string()
        server.sendmail(email_source, email_target, text)
        server.quit()

        trade_log.close()
