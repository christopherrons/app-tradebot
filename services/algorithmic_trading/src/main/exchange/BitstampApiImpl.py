from services.algorithmic_trading.src.main.calculators.CurrencyConverter import \
    CurrencyConverter
from services.algorithmic_trading.src.main.exchange.ExchangeApi import ExchangeApi
from services.algorithmic_trading.src.main.exchange.ExchangeService import ExchangeService
from services.algorithmic_trading.src.main.exchange.utils.BitstampAPIUtils import \
    APIBuyLimitOrder, APIOrderStatus, APITransactionFee, \
    APIAccountQuantity, APIAccountCash, APISellLimitOrder, APIOpenOrders, APIUserTransactions, APIError


class BitstampApiImpl(ExchangeApi):

    def __init__(self,
                 cash_currency: str,
                 crypto_currency: str,
                 customer_id: str,
                 api_key: str,
                 api_secret: str):
        self.__customer_id = bytes(customer_id, 'utf-8')
        self.__api_key = bytes(api_key, 'utf-8')
        self.__api_secret = bytes(api_secret, 'utf-8')

        self.__currency_converter = CurrencyConverter()
        self.__api_order_tries = 25

        super().__init__(exchange_name="Bitstamp",
                         cash_currency=cash_currency,
                         crypto_currency=crypto_currency)

    def execute_sell_order(self, price: float, quantity: float) -> str:
        order_id = ""
        for i in range(0, self.__api_order_tries):
            while True:
                try:
                    order_id = APISellLimitOrder(self.__customer_id, self.__api_key, self.__api_secret).call(
                        price=round(price, 5),
                        amount=round(quantity, 8),
                        fok_order=True)
                except APIError:
                    continue
                break

        return order_id

    def execute_buy_order(self, price: float, quantity: float) -> str:
        order_id = ""
        for i in range(0, self.__api_order_tries):
            while True:
                try:
                    order_id = APIBuyLimitOrder(self.__customer_id, self.__api_key, self.__api_secret).call(
                        price=round(price, 5),
                        amount=round(quantity, 8),
                        fok_order=True)
                except APIError:
                    continue
                break

        return order_id

    def get_account_cash_value(self) -> float:
        return float(APIAccountCash(self.__customer_id, self.__api_key, self.__api_secret).call())

    def get_account_quantity(self) -> float:
        return float(APIAccountQuantity(self.__customer_id, self.__api_key, self.__api_secret).call())

    def get_order_status(self, order_id: str) -> str:
        return APIOrderStatus(self.__customer_id, self.__api_key, self.__api_secret).call(id=order_id)

    def get_open_orders(self) -> list:
        return APIOpenOrders(self.__customer_id, self.__api_key, self.__api_secret).call()

    def get_transaction_fee(self, order_id: str) -> float:
        return float(APITransactionFee(self.__customer_id, self.__api_key, self.__api_secret).call(id=order_id))

    def get_transactions(self) -> list:
        return APIUserTransactions(self.__customer_id, self.__api_key, self.__api_secret).call(limit=1000)

    def get_accrued_account_fees(self) -> float:
        accrued_fee = 0
        for transaction in self.get_transactions():
            if transaction['usd'] != 0:
                if self._cash_currency.lower() == 'usd':
                    accrued_fee += float(transaction['fee'])
                else:
                    accrued_fee += self.__currency_converter.convert_currency(value=float(transaction['fee']),
                                                                              from_currency='usd',
                                                                              to_currency=self._cash_currency)
            else:
                if self._cash_currency.lower() == 'eur':
                    accrued_fee += float(transaction['fee'])
                else:
                    accrued_fee += self.__currency_converter.convert_currency(value=float(transaction['fee']),
                                                                              from_currency='eur',
                                                                              to_currency=self._cash_currency)

        return accrued_fee

    def get_successful_cycles(self) -> int:
        successful_cycles = 0
        for transaction in self.get_transactions():
            if transaction['type'] == '2':
                if float(transaction['usd']) > 0 or float(transaction['eur']) > 0:
                    successful_cycles += 1
        return successful_cycles

    def get_successful_trades(self) -> int:
        successful_trade = 0
        for transaction in self.get_transactions():
            if transaction['type'] == '2':
                successful_trade += 1
        return successful_trade

    def is_order_successful(self, order_id: str) -> bool:
        return self.get_order_status(order_id) != "Canceled"

    def is_order_status_open(self, order_id: str) -> bool:
        return self.get_order_status(order_id) == "Open"


