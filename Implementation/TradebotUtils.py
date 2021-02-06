import argparse
import os
from configparser import ConfigParser


class TradeBotUtils:
    @staticmethod
    class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
        pass

    @staticmethod
    def get_bitstamp_token():
        if not os.path.exists(os.path.expanduser('~') + '/.script-config'):
            raise ValueError('No configuration file exists. Expected file: ~/.script-config')

        config = ConfigParser()
        config.read(os.path.expanduser('~') + '/.script-config')
        return config.get('Bitstamp', 'Token')

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
