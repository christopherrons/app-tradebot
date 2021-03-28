from applications.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils
from applications.common.src.main.exchanges.KrakenApiImpl import KrakenApiImpl
from applications.common.src.main.exchanges.KrakenWebsocket import KrakenWebsocket


def main():
    exchange_api = KrakenApiImpl('usd',
                                 'xrp',
                                 TradeBotUtils.get_kraken_api_key(),
                                 TradeBotUtils.get_kraken_api_secret())
    # OKAP47-224CI-NICW7F
    #trade_id = exchange_api.execute_sell_order(0.55317, 45)
    #trade_id = "OTWRX5-3JUAD-HTURHJ"
    #print(exchange_api.is_order_status_open(trade_id))
    #print(exchange_api.is_order_successful(trade_id))
    closed_transactions = exchange_api.get_transactions()
    trade_nr = 1
    for idx, order_id in enumerate(closed_transactions.keys()):
        if closed_transactions[order_id]['status'] == "closed":
            print(closed_transactions[order_id])



if __name__ == '__main__':
    main()
