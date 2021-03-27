from applications.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils
from applications.common.src.main.exchanges.KrakenApiImpl import KrakenApiImpl
from applications.common.src.main.exchanges.KrakenWebsocket import KrakenWebsocket


def main():
    exchange_api = KrakenApiImpl('usd',
                                 'xrp',
                                 TradeBotUtils.get_kraken_api_key(),
                                 TradeBotUtils.get_kraken_api_secret())
    # OKAP47-224CI-NICW7F
    #trade_id = exchange_api.execute_buy_order(0.2, 40)
    #print(exchange_api.is_order_status_open(trade_id))



if __name__ == '__main__':
    main()
