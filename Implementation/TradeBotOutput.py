import csv
import os
from datetime import datetime
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from tabulate import tabulate
from Calculator import Calculator
from Utils.TradebotUtils import TradeBotUtils


class TradeBotOutput:

    def __init__(self, trade_bot_cache, is_reset_logs):
        self.__trade_bot_cache = trade_bot_cache
        self.__is_reset_logs = is_reset_logs
        self.__current_formation_log_file = os.path.realpath(__file__).replace("Implementation/TradeBotOutput.py",
                                                                               "logs/current_formation_log.csv")  # Shitty solution
        self.__successful_trade_log = os.path.realpath(__file__).replace("Implementation/TradeBotOutput.py",
                                                                         "logs/trades_logs.csv")  # Shitty solution
        self.__calculator = Calculator(trade_bot_cache)

    def print_and_log_current_formation(self, is_buy):
        if is_buy:
            account_trade = "Account Bid Price [$]"
            account_trade_price = self.__trade_bot_cache.account_bid_price

            market_trade = "Market Ask Price [$]"
            market_trade_price = self.__trade_bot_cache.market_ask_price

            current_value_description = "Current Value (Cash)"
            current_value = self.__trade_bot_cache.cash_value

            net_profit = "Cash Profit [$]"
            net_profit_value = self.__calculator.net_cash_profit()

            percent_profit = "Cash Profit [%]"
            percent_profit_value = self.__calculator.percent_cash_profit()

        else:
            account_trade = "Account Ask Price [$]"
            account_trade_price = self.__trade_bot_cache.account_ask_price

            market_trade = "Market Bid Price [$]"
            market_trade_price = self.__trade_bot_cache.market_bid_price

            current_value_description = "Current Value (Position)"
            current_value = self.__trade_bot_cache.position_value

            net_profit = "Position Profit [$]"
            net_profit_value = self.__calculator.net_position_profit()

            percent_profit = "Position Profit [%]"
            percent_profit_value = self.__calculator.percent_position_profit()

        headers = ['Timestamp', account_trade, market_trade, 'Nr Successfully cycles', 'Initial Value [$]',
                   current_value_description, percent_profit, 'Accrued Fees [$]']

        output = [datetime.now(), account_trade_price,
                  market_trade_price, self.__trade_bot_cache.successful_cycles,
                  self.__trade_bot_cache.initial_value, current_value,
                  percent_profit_value, self.__trade_bot_cache.accrued_fee]

        self.print_data(headers, output)

        headers[1] = "Account Trade Price"
        headers[2] = "Market Trade Price"
        headers.insert(1, "Is Buy")
        output.insert(1, is_buy)
        self.log_data(headers, output, self.__current_formation_log_file)

    def print_and_log_successful_trades(self, is_buy, fee):
        if is_buy:
            value = self.__trade_bot_cache.cash_value
            quantity = self.__trade_bot_cache.buy_quantity
            price = self.__trade_bot_cache.market_ask_price
        else:
            value = self.__trade_bot_cache.position_value
            quantity = self.__trade_bot_cache.sell_quantity
            price = self.__trade_bot_cache.market_bid_price

        headers = ['Timestamp', 'Is Buy', 'Value', 'Price', 'Quantity', 'Fee [$]']
        output = [datetime.now(), is_buy, value, price, quantity, fee]
        self.print_data(headers, output)
        self.log_data(headers, output, self.__successful_trade_log)

    def print_data(self, headers, output):
        tabulated_output = tabulate([output], headers=headers)
        print(tabulated_output + "\n\n\n\n\n\n")

    def log_data(self, headers, output, file):
        with open(file, 'a+') as f:
            writer = csv.writer(f)
            if self.__is_reset_logs:
                f.truncate(0)
                self.__is_reset_logs = False
            if os.stat(file).st_size == 0:
                writer.writerow(headers)
                writer.writerow(output)
            else:
                writer.writerow(output)

    def send_email(self):
        email_source = TradeBotUtils.get_email_source()
        email_source_password = TradeBotUtils.get_email_source_password()
        email_target = TradeBotUtils.get_email_target()

        message = MIMEMultipart()
        message['From'] = email_source
        message['To'] = email_target
        message['Subject'] = "Trade Occured"
        message.attach(MIMEText('Trade Occured test', 'plain'))

        current_information_log = open(self.__current_formation_log_file, "rb")
        trade_log = open(self.__successful_trade_log, "rb")

        part_information = MIMEBase('applications', 'octet-stream')
        part_information.set_payload(current_information_log.read())
        encoders.encode_base64(part_information)
        part_information.add_header('Content-Disposition',
                                    'attachment; filename=%s' % os.path.basename(self.__current_formation_log_file))
        message.attach(part_information)

        part_trade = MIMEBase('applications', 'octet-stream')
        part_trade.set_payload(trade_log.read())
        encoders.encode_base64(part_information)
        part_trade.add_header('Content-Disposition',
                              'attachment; filename=%s' % os.path.basename(self.__successful_trade_log))
        message.attach(part_trade)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        server.login(email_source, email_source_password)
        text = message.as_string()
        server.sendmail(email_source, email_target, text)
        server.quit()

        current_information_log.close()
        trade_log.close()


