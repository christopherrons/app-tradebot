from Services.Runner.Calculators.CurrencyConverter import CurrencyConverter
from Services.Runner.Exchange.ExchangeApi import ExchangeApi
from Services.Runner.Exchange.Utils.KrakenAPIUtils import APIBuyLimitOrder, APIOrderStatus, APITransactionFee, \
    APIAccountQuantity, APIAccountCash, APISellLimitOrder, APIOpenOrders, APIUserTransactions


class KrakenApiImpl(ExchangeApi):

    def __init__(self,
                 cash_currency,
                 crypto_currency,
                 exchange_websocket,
                 api_key,
                 api_secret):
        self.cash_currency = cash_currency
        self.crypto_currency = crypto_currency
        self.exchange_websocket = exchange_websocket
        self.api_key = str(api_key)
        self.api_secret = str(api_secret)

        self.currency_converter = CurrencyConverter()

    def sell_action(self, price, quantity):
        return APISellLimitOrder(self.api_key, self.api_secret).call(price=round(price, 5),
                                                                     amount=quantity,
                                                                     fok_order=True)

    def buy_action(self, price, quantity):
        return APIBuyLimitOrder(self.api_key, self.api_secret).call(price=round(price, 5),
                                                                    amount=round(quantity, 8),
                                                                    fok_order=True)

    def get_account_cash_value(self):
        return float(APIAccountCash(self.api_key, self.api_secret).call())

    def get_account_quantity(self):
        return float(APIAccountQuantity(self.api_key, self.api_secret).call())

    def get_order_status(self, order_id):
        orders = APIOrderStatus(self.api_key, self.api_secret).call(refid=order_id)
        for status_keys in orders:
            if order_id in orders[status_keys]:
                return str(status_keys)
        return "Not found"

    def get_open_orders(self):
        return APIOpenOrders(self.api_key, self.api_secret).call()

    def get_transaction_fee(self, order_id):
        return float(APITransactionFee(self.api_key, self.api_secret).call(userref=order_id))

    def get_transactions(self):
        return APIUserTransactions(self.api_key, self.api_secret).call()

    def get_accrued_account_fees(self):
        accrued_fee = 0
        closed_transactions = self.get_transactions()['closed']
        for transaction in closed_transactions.keys():
            transaction_currency = closed_transactions[transaction]['descr']['pair']
            print(transaction_currency)
            if self.cash_currency in transaction_currency:
                accrued_fee += float(closed_transactions[transaction]['fee'])
            else:
                accrued_fee += self.currency_converter.convert_currency(value=float(closed_transactions[transaction]['fee']),
                                                                        from_currency='USD' if 'USD' in transaction_currency else 'EUR',
                                                                        to_currency=self.cash_currency)
        return accrued_fee

    def get_successful_cycles(self):
        successful_cycles = 0
        closed_transactions = self.get_transactions()['closed']
        for transaction in closed_transactions.keys():
            if closed_transactions[transaction]['descr']['type'] == 'sell':
                successful_cycles += 1
        return successful_cycles

    def get_successful_trades(self):
        return self.get_transactions()['count']

    def is_order_successful(self, order_id):
        order_status = self.get_order_status(order_id)
        return order_status != 'canceled' and order_status != 'expired'

    def is_order_status_open(self, order_id):
        order_status = self.get_order_status(order_id)
        return order_status == 'open' or order_status == 'pending'

    def get_exchange_name(self):
        return "Kraken"
