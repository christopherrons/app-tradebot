import redis

from applications.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils
from applications.common.src.main.exchanges.KrakenApi import KrakenApi


def main():
    exchange_api = KrakenApi('usd',
                             'xrp',
                             TradeBotUtils.get_kraken_api_key(),
                             TradeBotUtils.get_kraken_api_secret())
    tr = exchange_api.get_transactions()

    for key in tr.keys():
        print(key)


if __name__ == '__main__':
    main()
