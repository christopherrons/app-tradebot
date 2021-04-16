from applications.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils
from applications.common.src.main.exchanges.KrakenApi import KrakenApi


def main():
    exchange_api = KrakenApi('usd',
                             'xlm',
                             TradeBotUtils.get_kraken_api_key(),
                             TradeBotUtils.get_kraken_api_secret())
    print(exchange_api.get_card_payments())


if __name__ == '__main__':
    main()
