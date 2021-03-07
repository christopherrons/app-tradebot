import argparse
import os
import smtplib
from configparser import ConfigParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class TradeBotUtils:
    @staticmethod
    class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
        pass

    @staticmethod
    def reset_logs():
        for file in [TradeBotUtils.get_trade_log_path(), TradeBotUtils.get_information_log_path()]:
            with open(file, 'a+') as f:
                f.truncate(0)

    @staticmethod
    def get_trade_log_path():
        return os.path.realpath(__file__).replace("Services/Runner/Utils/TradeBotUtils.py",
                                                  "logs/trades_logs.csv")

    @staticmethod
    def get_information_log_path():
        return os.path.realpath(__file__).replace("Services/Runner/Utils/TradeBotUtils.py",
                                                  "logs/current_formation_log.csv")

    @staticmethod
    def get_script_config_attribute(parent, attribute):
        if not os.path.exists(os.path.expanduser('~') + '/.script-config'):
            raise ValueError('No configuration file exists. Expected file: ~/.script-config')

        config = ConfigParser()
        config.read(os.path.expanduser('~') + '/.script-config')
        return config.get(parent, attribute)

    @staticmethod
    def get_email_source():
        return TradeBotUtils.get_script_config_attribute('User', 'emailSource')

    @staticmethod
    def get_email_source_password():
        return TradeBotUtils.get_script_config_attribute('User', 'emailSourcePassword')

    @staticmethod
    def get_email_target():
        return TradeBotUtils.get_script_config_attribute('User', 'emailTarget')

    @staticmethod
    def get_kraken_api_secret():
        return TradeBotUtils.get_script_config_attribute('Kraken', 'apiSecret')

    @staticmethod
    def get_kraken_api_key():
        return TradeBotUtils.get_script_config_attribute('Kraken', 'apiKey')

    @staticmethod
    def get_bitstamp_api_secret():
        return TradeBotUtils.get_script_config_attribute('Bitstamp', 'apiSecret')

    @staticmethod
    def get_bitstamp_api_key():
        return TradeBotUtils.get_script_config_attribute('Bitstamp', 'apiKey')

    @staticmethod
    def get_bitstamp_customer_ID():
        return TradeBotUtils.get_script_config_attribute('Bitstamp', 'customerID')

    @staticmethod
    def is_run_time_passed(current_time, run_stop_time):
        return current_time > run_stop_time

    @staticmethod
    def live_run_checker(is_not_simulation):
        if is_not_simulation:
            contract = input("WARNING LIVE RUN. If you want to trade sign the contract with: winteriscoming: ")
            if contract != "winteriscoming":
                print("ABORTING")
                exit()
            else:
                print("Contracted signed! Live run accepted!\n")

    @staticmethod
    def validate_args(args, minimum_interest):
        if args.initial_value < 1:
            raise ValueError(f'Initial Value {args.initial_value} is to low. Minimum value is 1')

        if args.interest < minimum_interest:
            raise ValueError(f'Interest {args.interest} is to low. Minimum value is 0.{minimum_interest}')

        if args.print_interval < 0:
            raise ValueError(f'Print Interval {args.print_interval} is to low. Minimum value is 0')

        if args.run_time_minutes < 1:
            raise ValueError(f'Run Time {args.run_time_minutes} is to low. Minimum value is 1')

        if args.run_time_minutes > 1000000:
            raise ValueError(f'Print Interval {args.run_time_minutes} is to high. Maximum value is 1000000')

    @staticmethod
    def set_initial_trade_price(bitstamp_api, is_sell):
        is_invalid_account_trade_price = True
        while is_invalid_account_trade_price:
            market_bid_price = bitstamp_api.get_market_bid_price()
            market_ask_price = bitstamp_api.get_market_ask_price()
            print(f'Market bid: {market_bid_price} \nMarket ask: {market_ask_price}\n')

            if is_sell:
                account_trade_price = float(input('Set start account ASK price: '))
                is_invalid_account_trade_price = TradeBotUtils.is_invalid_account_ask_price(market_bid_price,
                                                                                            account_trade_price)
                if is_invalid_account_trade_price:
                    print("ERROR: Account ask price has to be larger than market bid price.\n")
                else:
                    print(f"Account Ask Price: {account_trade_price}\n")
            else:
                account_trade_price = float(input('Set start account BID price: '))
                is_invalid_account_trade_price = TradeBotUtils.is_invalid_account_bid_price(market_ask_price,
                                                                                            account_trade_price)
                if is_invalid_account_trade_price:
                    print("ERROR: Account bid price has to be smaller than market ask price.\n")
                else:
                    print(f"Account Bid Price: {account_trade_price}\n")

        return account_trade_price

    @staticmethod
    def is_invalid_account_bid_price(market_ask_price, account_bid_price):
        return market_ask_price - account_bid_price < 0

    @staticmethod
    def is_invalid_account_ask_price(market_bid_price, account_ask_price):
        return market_bid_price - account_ask_price > 0

    @staticmethod
    def send_error_has_occurred_email(exchange, error):
        email_source = TradeBotUtils.get_email_source()
        email_source_password = TradeBotUtils.get_email_source_password()
        email_target = TradeBotUtils.get_email_target()

        message = MIMEMultipart()
        message['From'] = email_source
        message['To'] = email_target
        message['Subject'] = f"{exchange}: Error has occurred"
        message.attach(MIMEText(f'{error}'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        server.login(email_source, email_source_password)
        text = message.as_string()
        server.sendmail(email_source, email_target, text)
        server.quit()

    @staticmethod
    def get_cash_currency_symbols():
        return {
            'USD': '$',
            'EUR': '€'
        }
