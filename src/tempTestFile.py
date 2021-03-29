from applications.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils
from applications.common.src.main.exchanges.KrakenApi import KrakenApi
from applications.common.src.main.exchanges.KrakenWebsocket import KrakenWebsocket


def main():
    exchange_api = KrakenApi('usd',
                                 'xrp',
                             TradeBotUtils.get_kraken_api_key(),
                             TradeBotUtils.get_kraken_api_secret())
    websocket = KrakenWebsocket('usd', 'xrp')
    websocket.reconnect()


if __name__ == '__main__':
    main()
