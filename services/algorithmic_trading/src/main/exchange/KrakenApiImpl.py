from services.algorithmic_trading.src.main.calculators.CurrencyConverter import \
    CurrencyConverter
from services.algorithmic_trading.src.main.exchange.ExchangeApi import ExchangeApi
from services.algorithmic_trading.src.main.exchange.ExchangeWebsocket import ExchangeWebsocket
from services.algorithmic_trading.src.main.exchange.utils.KrakenAPIUtils import \
    APIBuyLimitOrder, APIOrderStatus, APITransactionFee, \
    APIAccountQuantity, APIAccountCash, APISellLimitOrder, APIOpenOrders, APIUserTransactions


class KrakenApiImpl(ExchangeApi):

    def __init__(self,
                 cash_currency: str,
                 crypto_currency: str,
                 exchange_websocket: ExchangeWebsocket,
                 api_key: str,
                 api_secret: str):
        self.__cash_currency = cash_currency
        self.__crypto_currency = crypto_currency
        self.__exchange_websocket = exchange_websocket
        self.__api_key = str(api_key)
        self.__api_secret = str(api_secret)

        self.__currency_converter = CurrencyConverter()
        self.__exchange_name = "Kraken"

    def sell_action(self, price: float, quantity: float) -> str:
        return APISellLimitOrder(self.__api_key, self.__api_secret).call(price=round(price, 5),
                                                                         amount=quantity,
                                                                         fok_order=True)

    def buy_action(self, price: float, quantity: float) -> str:
        return APIBuyLimitOrder(self.__api_key, self.__api_secret).call(price=round(price, 5),
                                                                        amount=round(quantity, 8),
                                                                        fok_order=True)

    def get_account_cash_value(self) -> float:
        return float(APIAccountCash(self.__api_key, self.__api_secret).call())

    def get_account_quantity(self) -> float:
        return float(APIAccountQuantity(self.__api_key, self.__api_secret).call())

    def get_order_status(self, order_id: str) -> str:
        orders = APIOrderStatus(self.__api_key, self.__api_secret).call(refid=order_id)
        for status_keys in orders:
            if order_id in orders[status_keys]:
                return str(status_keys)
        return "Not found"

    def get_open_orders(self) -> list:
        return APIOpenOrders(self.__api_key, self.__api_secret).call()

    def get_transaction_fee(self, order_id: str) -> float:
        return float(APITransactionFee(self.__api_key, self.__api_secret).call(userref=order_id))

    def get_transactions(self) -> dict:
        return APIUserTransactions(self.__api_key, self.__api_secret).call()

    def get_accrued_account_fees(self) -> float:
        accrued_fee = 0
        closed_transactions = self.get_transactions()['closed']
        for transaction in closed_transactions.keys():
            transaction_currency = closed_transactions[transaction]['descr']['pair']
            print(transaction_currency)
            if self.cash_currency in transaction_currency:
                accrued_fee += float(closed_transactions[transaction]['fee'])
            else:
                accrued_fee += self.__currency_converter.convert_currency(
                    value=float(closed_transactions[transaction]['fee']),
                    from_currency='USD' if 'USD' in transaction_currency else 'EUR',
                    to_currency=self.cash_currency)
        return accrued_fee

    def get_successful_cycles(self) -> int:
        successful_cycles = 0
        closed_transactions = self.get_transactions()['closed']
        for transaction in closed_transactions.keys():
            if closed_transactions[transaction]['descr']['type'] == 'sell':
                successful_cycles += 1
        return successful_cycles

    def get_successful_trades(self) -> int:
        return self.get_transactions()['count']

    def is_order_successful(self, order_id: str) -> bool:
        order_status = self.get_order_status(order_id)
        return order_status != 'canceled' and order_status != 'expired'

    def is_order_status_open(self, order_id: str) -> bool:
        order_status = self.get_order_status(order_id)
        return order_status == 'open' or order_status == 'pending'

    @property
    def exchange_name(self) -> str:
        return self.exchange_name

    @exchange_name.setter
    def exchange_name(self, exchange_name: str):
        self.__exchange_name = exchange_name

    @property
    def cash_currency(self) -> str:
        return self.cash_currency

    @cash_currency.setter
    def cash_currency(self, cash_currency: str):
        self.__cash_currency = cash_currency

    @property
    def crypto_currency(self) -> str:
        return self.crypto_currency

    @crypto_currency.setter
    def crypto_currency(self, crypto_currency):
        self.__crypto_currency = crypto_currency
