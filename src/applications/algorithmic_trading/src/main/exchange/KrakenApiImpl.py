from datetime import datetime

from applications.algorithmic_trading.src.main.calculators.CurrencyConverter import \
    CurrencyConverter
from applications.algorithmic_trading.src.main.database.DatabaseService import DatabaseService
from applications.algorithmic_trading.src.main.exchange.ExchangeApi import ExchangeApi
from applications.algorithmic_trading.src.main.exchange.utils.KrakenAPIUtils import \
    APIBuyLimitOrder, APIOrderStatus, APITransactionFee, \
    APIAccountQuantity, APIAccountCash, APISellLimitOrder, APIOpenOrders, APIUserTransactions
from applications.algorithmic_trading.src.main.output_handlers.utils.PrinterUtils import PrinterUtils
from applications.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils


class KrakenApiImpl(ExchangeApi):

    def __init__(self,
                 cash_currency: str,
                 crypto_currency: str,
                 api_key: str,
                 api_secret: str):
        self.__api_key = str(api_key)
        self.__api_secret = str(api_secret)

        self.__currency_converter = CurrencyConverter()

        super().__init__(exchange_name="kraken",
                         cash_currency=cash_currency,
                         crypto_currency=crypto_currency)

    def execute_sell_order(self, price: float, quantity: float) -> str:
        return APISellLimitOrder(self.__api_key, self.__api_secret).call(price=round(price, 5),
                                                                         amount=quantity,
                                                                         fok_order=True)

    def execute_buy_order(self, price: float, quantity: float) -> str:
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

    def is_order_successful(self, order_id: str) -> bool:
        order_status = self.get_order_status(order_id)
        return order_status != 'canceled' and order_status != 'expired'

    def is_order_status_open(self, order_id: str) -> bool:
        order_status = self.get_order_status(order_id)
        return order_status == 'open' or order_status == 'pending'

    def get_transaction_timestamp(self, transaction: dict) -> datetime:
        return TradeBotUtils.convert_epoch_time_to_timestamp(transaction['closetm'])

    def is_transaction_buy(self, transaction: dict) -> bool:
        return False if transaction['descr']['type'] == 'sell' else True

    def get_transaction_cash_currency(self, transaction: dict) -> str:
        for cash_currency in TradeBotUtils.get_permitted_cash_currencies():
            if cash_currency in transaction['descr']['pair']:
                return cash_currency
        return 'fail'

    def get_transaction_crypto_currency(self, transaction: dict) -> str:
        for crypto_currency in TradeBotUtils.get_permitted_crypto_currencies():
            if crypto_currency in transaction['descr']['pair']:
                return crypto_currency
        return 'fail'

    def get_transaction_fee_from_transaction_dict(self, transaction: dict) -> float:
        return float(transaction['fee'])

    def get_transaction_price_per_quantity(self, transaction: dict) -> float:
        return float(transaction['descr']['price'])

    def get_transaction_quantity(self, transaction: dict) -> float:
        return float(transaction['vol'])

    def get_transaction_gross_value(self, transaction: dict) -> float:
        return self.get_transaction_price_per_quantity(transaction) * self.get_transaction_quantity(transaction)

    def get_transaction_net_value(self, transaction: dict) -> float:
        return self.get_transaction_gross_value(transaction) - self.get_transaction_fee_from_transaction_dict(transaction)

    def init_database_from_exchange(self, database_service: DatabaseService):
        PrinterUtils.console_log(message=f"Initializing Database from kraken!")
        closed_transactions = self.get_transactions()['closed']
        for idx, order_id in enumerate(closed_transactions.keys()):
            database_service.insert_trade_report(order_id=order_id,
                                                 is_live=True, exchange='kraken',
                                                 timestamp=self.get_transaction_timestamp(closed_transactions[order_id]),
                                                 buy=self.is_transaction_buy(closed_transactions[order_id]),
                                                 cash_currency=self.get_transaction_cash_currency(closed_transactions[order_id]),
                                                 crypto_currency=self.get_transaction_crypto_currency(closed_transactions[order_id]),
                                                 fee=self.get_transaction_fee_from_transaction_dict(closed_transactions[order_id]),
                                                 price=self.get_transaction_price_per_quantity(closed_transactions[order_id]),
                                                 quantity=self.get_transaction_quantity(closed_transactions[order_id]),
                                                 gross_trade_value=self.get_transaction_gross_value(closed_transactions[order_id]),
                                                 net_trade_value=self.get_transaction_net_value(closed_transactions[order_id]))
