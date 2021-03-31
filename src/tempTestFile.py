from applications.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils
from applications.common.src.main.exchanges.KrakenApi import KrakenApi
from applications.common.src.main.exchanges.KrakenWebsocket import KrakenWebsocket


def main():
    exchange_api = KrakenApi('usd',
                                 'xrp',
                             TradeBotUtils.get_kraken_api_key(),
                             TradeBotUtils.get_kraken_api_secret())
    print(exchange_api.is_order_status_open("O2JRT4-FGEFL-XZQJNJ"))


if __name__ == '__main__':
    main()
