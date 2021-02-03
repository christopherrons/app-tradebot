import argparse
import os
from configparser import ConfigParser


class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass


def get_bitstamp_token():
    if not os.path.exists(os.path.expanduser('~') + '/.script-config'):
        raise ValueError('No configuration file exists. Expected file: ~/.script-config')

    config = ConfigParser()
    config.read(os.path.expanduser('~') + '/.script-config')
    return config.get('Bitstamp', 'Token')
