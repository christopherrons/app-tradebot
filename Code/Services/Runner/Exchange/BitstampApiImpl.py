from Services.Runner.Exchange.ExchangeApi import ExchangeApi
from Services.Runner.Exchange.Utils.BitstampAPIUtils import APIBuyLimitOrder, APIOrderStatus, APITransactionFee, \
    APIAccountQuantity, APIAccountCash, APISellLimitOrder, APIOpenOrders, APIUserTransactions


class BitstampApiImpl(ExchangeApi):

    def __init__(self, exchange_websocket, customer_id, api_key, api_secret):
        self.exchange_websocket = exchange_websocket
        self.customer_id = bytes(customer_id, 'utf-8')
        self.api_key = bytes(api_key, 'utf-8')
        self.api_secret = bytes(api_secret, 'utf-8')

    def sell_action(self, price, quantity):
        return APISellLimitOrder(self.customer_id, self.api_key, self.api_secret).call(price=round(price, 5),
                                                                                       amount=quantity,
                                                                                       fok_order=True)

    def buy_action(self, price, quantity):
        return APIBuyLimitOrder(self.customer_id, self.api_key, self.api_secret).call(price=round(price, 5),
                                                                                      amount=round(quantity, 8),
                                                                                      fok_order=True)

    def get_account_cash_value(self):
        return float(APIAccountCash(self.customer_id, self.api_key, self.api_secret).call())

    def get_account_quantity(self):
        return float(APIAccountQuantity(self.customer_id, self.api_key, self.api_secret).call())

    def get_order_status(self, order_id):
        return APIOrderStatus(self.customer_id, self.api_key, self.api_secret).call(id=order_id)

    def get_open_orders(self):
        return APIOpenOrders(self.customer_id, self.api_key, self.api_secret).call()

    def get_transaction_fee(self, order_id):
        return float(APITransactionFee(self.customer_id, self.api_key, self.api_secret).call(id=order_id))

    def get_transactions(self):
        return APIUserTransactions(self.customer_id, self.api_key, self.api_secret).call(limit=1000)

    def get_accrued_account_fees(self):
        accrued_fee = 0
        for transaction in self.get_transactions():
            accrued_fee += float(transaction['fee'])
        return accrued_fee

    def get_successful_cycles(self):
        successful_cycles = 0
        for transaction in self.get_transactions():
            if transaction['type'] == '2':
                if float(transaction['usd']) > 0:
                    successful_cycles += 1
        return successful_cycles

    def get_successful_trades(self):
        successful_trade = 0
        for transaction in self.get_transactions():
            if transaction['type'] == '2':
                successful_trade += 1
        return successful_trade

    def is_order_successful(self, order_id):
        return self.get_order_status(order_id) != "Canceled"

    def is_order_status_open(self, order_id):
        return self.get_order_status(order_id) == "Open"

    def get_exchange_name(self):
        return "Bitstamp"