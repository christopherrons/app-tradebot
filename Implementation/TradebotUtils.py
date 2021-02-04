import argparse
import os
from configparser import ConfigParser
import time


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
