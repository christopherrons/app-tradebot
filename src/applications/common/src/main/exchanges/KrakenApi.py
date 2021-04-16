import time
from datetime import datetime

from applications.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils
from applications.common.src.main.converters.CurrencyConverter import \
    CurrencyConverter
from applications.common.src.main.database import DatabaseService
from applications.common.src.main.exchanges.ExchangeApi import ExchangeApi
from applications.common.src.main.exchanges.utils.ExchangeUtils import ExchangeUtils
from applications.common.src.main.exchanges.utils.KrakenApiUtils import \
    APIBuyLimitOrder, APITransactionFee, \
    APIAccountQuantity, APIAccountCash, APISellLimitOrder, APIOpenOrders, APIOrderStatus, APIClosedOrders, APIOrderCancelReason, APIQueryLedger
from applications.common.src.main.utils.PrinterUtils import PrinterUtils


class KrakenApi(ExchangeApi):

    def __init__(self,
                 cash_currency: str,
                 crypto_currency: str,
                 api_key: str,
                 api_secret: str):
        self.__api_key = str(api_key)
        self.__api_secret = str(api_secret)

        self.__currency_converter = CurrencyConverter()
        self.__kraken_currency_names = {
            "xrp": "XXRP",
            "usd": "ZUSD",
            "xlm": "XXLM"
        }

        super().__init__(exchange_name="kraken",
                         cash_currency=cash_currency,
                         crypto_currency=crypto_currency)

    def execute_sell_order(self, price: float, quantity: float) -> str:
        return APISellLimitOrder(self.__api_key, self.__api_secret).call(pair=f"{self.crypto_currency.upper()}/{self.cash_currency.upper()}",
                                                                         price=round(price, 5),
                                                                         volume=quantity,
                                                                         type="sell",
                                                                         ordertype="limit",
                                                                         oflags="post")

    def execute_buy_order(self, price: float, quantity: float) -> str:
        return APIBuyLimitOrder(self.__api_key, self.__api_secret).call(pair=f"{self.crypto_currency.upper()}/{self.cash_currency.upper()}",
                                                                        price=round(price, 5),
                                                                        volume=round(quantity, 8),
                                                                        type="buy",
                                                                        ordertype="limit",
                                                                        oflags="post")

    def get_account_cash_value(self) -> float:
        return float(APIAccountCash(self.__api_key, self.__api_secret).call()[self.__kraken_currency_names[self.cash_currency.lower()]])

    def get_account_quantity(self) -> float:
        quantities = APIAccountQuantity(self.__api_key, self.__api_secret).call()
        return float(quantities[self.__kraken_currency_names[self.crypto_currency.lower()]]) \
            if self.__kraken_currency_names[self.crypto_currency.lower()] in quantities.keys() \
            else 0

    def get_order_status(self, order_id: str) -> str:
        return APIOrderStatus(self.__api_key, self.__api_secret).call(txid=order_id)

    def get_open_orders(self) -> list:
        return APIOpenOrders(self.__api_key, self.__api_secret).call()

    def get_transaction_fee(self, order_id: str) -> float:
        return float(APITransactionFee(self.__api_key, self.__api_secret).call(txid=order_id))

    def get_transactions(self) -> dict:
        transactions = dict()
        end_time = time.time()
        while True:
            result = APIClosedOrders(self.__api_key, self.__api_secret).call(start=0,
                                                                             end=end_time)
            if result:
                transactions.update(result)
                end_time = self.__get_earliest_timestamp_from_transactions(result, end_time, 'closetm')
            else:
                break
            time.sleep(1.5)
        transactions.update(self.__get_card_payments())
        return transactions

    def __get_card_payments(self) -> dict:
        return self.__combine_received_and_send_transactions()

    def __combine_received_and_send_transactions(self) -> dict:
        ledger_entries = self.__query_ledger()
        transactions = dict()
        for key in ledger_entries.keys():
            if ledger_entries[key]['type'] == 'receive':
                if ledger_entries[key]['refid'] in transactions.keys():
                    transactions[ledger_entries[key]['refid']] = {**{
                        'refid': ledger_entries[key]['refid'],
                        'status': 'closed',
                        'opentm': ledger_entries[key]['time'],
                        'closetm': ledger_entries[key]['time'],
                        'vol': float(ledger_entries[key]['amount']),
                        'crypto_currency': ledger_entries[key]['asset'],
                        'type': 'buy'
                    }, **transactions[ledger_entries[key]['refid']]}
                else:
                    transactions[ledger_entries[key]['refid']] = {
                        'refid': ledger_entries[key]['refid'],
                        'status': 'closed',
                        'opentm': ledger_entries[key]['time'],
                        'closetm': ledger_entries[key]['time'],
                        'vol': float(ledger_entries[key]['amount']),
                        'crypto_currency': ledger_entries[key]['asset'],
                        'type': 'buy'
                    }

            elif ledger_entries[key]['type'] == 'spend':
                card_purchase_fee = 1.05
                if ledger_entries[key]['refid'] in transactions.keys():
                    transactions[ledger_entries[key]['refid']] = {**{
                        'fee': ledger_entries[key]['fee'],
                        'cost': card_purchase_fee * abs(float(ledger_entries[key]['amount'])),
                        'cash_currency': ledger_entries[key]['asset'].replace(".HOLD", ""),
                    }, **transactions[ledger_entries[key]['refid']]}
                else:
                    transactions[ledger_entries[key]['refid']] = {
                        'fee': ledger_entries[key]['fee'],
                        'cost': abs(float(ledger_entries[key]['amount'])),
                        'cash_currency': ledger_entries[key]['asset'].replace(".HOLD", ""),
                    }

        for key in transactions.keys():
            transactions[key]['descr'] = {
                'pair': transactions[key]['crypto_currency'] + transactions[key]['cash_currency'],
                'price': transactions[key]['cost'] / transactions[key]['vol'],
                'type': 'buy'
            }

        return transactions

    def __query_ledger(self) -> dict:
        ledger_entries = dict()
        end_time = time.time()
        while True:
            result = APIQueryLedger(self.__api_key, self.__api_secret).call(start=0,
                                                                            end=end_time)
            if result:
                ledger_entries.update(result)
                end_time = self.__get_earliest_timestamp_from_transactions(result, end_time, 'time')
            else:
                break
            time.sleep(1.5)
        return ledger_entries

    def __get_earliest_timestamp_from_transactions(self, result: dict, end_time: float, timestamp_name: str):
        for order_id in result.keys():
            transaction_end_time = result[order_id][timestamp_name]
            if transaction_end_time < end_time:
                end_time = transaction_end_time
        return end_time

    def is_order_successful(self, order_id: str) -> bool:
        order_status = self.get_order_status(order_id)
        if order_status != 'canceled':
            cancel_reason = APIOrderCancelReason(self.__api_key, self.__api_secret).call(txid=order_id)
            if cancel_reason == "Out of funds":
                return True
            else:
                return False
        return order_status != 'expired' and order_status == "closed"

    def is_order_status_open(self, order_id: str) -> bool:
        order_status = self.get_order_status(order_id)
        return order_status == 'open' or order_status == 'pending'

    def get_transaction_timestamp(self, transaction: dict) -> datetime:
        return TradeBotUtils.convert_epoch_time_to_timestamp(transaction['closetm'])

    def is_transaction_buy(self, transaction: dict) -> bool:
        return False if transaction['descr']['type'] == 'sell' else True

    def get_transaction_cash_currency(self, transaction: dict) -> str:
        for cash_currency in ExchangeUtils.get_permitted_cash_currencies():
            if cash_currency in transaction['descr']['pair'].lower():
                return cash_currency
        return 'fail'

    def get_transaction_crypto_currency(self, transaction: dict) -> str:
        for crypto_currency in ExchangeUtils.get_permitted_crypto_currencies():
            if crypto_currency in transaction['descr']['pair'].lower():
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

    def init_trades_to_database_from_exchange(self, database_service: DatabaseService):
        PrinterUtils.console_log(message=f"Initializing Database from kraken!")
        closed_transactions = self.get_transactions()
        trade_nr = 1
        for idx, order_id in enumerate(reversed(list(closed_transactions.keys()))):
            if self.__is_successful_order(closed_transactions, order_id):
                database_service.insert_trade_report(order_id=order_id,
                                                     is_live=True, exchange='kraken',
                                                     timestamp=self.get_transaction_timestamp(closed_transactions[order_id]),
                                                     trade_number=trade_nr,
                                                     buy=self.is_transaction_buy(closed_transactions[order_id]),
                                                     cash_currency=self.get_transaction_cash_currency(closed_transactions[order_id]),
                                                     crypto_currency=self.get_transaction_crypto_currency(closed_transactions[order_id]),
                                                     fee=self.get_transaction_fee_from_transaction_dict(closed_transactions[order_id]),
                                                     price=self.get_transaction_price_per_quantity(closed_transactions[order_id]),
                                                     quantity=self.get_transaction_quantity(closed_transactions[order_id]),
                                                     gross_trade_value=self.get_transaction_gross_value(closed_transactions[order_id]),
                                                     net_trade_value=self.get_transaction_net_value(closed_transactions[order_id]))
                trade_nr += 1

    def __is_successful_order(self, closed_transactions: dict, order_id: str) -> bool:
        return closed_transactions[order_id]['status'] == "closed" \
               or closed_transactions[order_id]['status'] == "canceled" and closed_transactions[order_id]['reason'] == "Out of funds"
