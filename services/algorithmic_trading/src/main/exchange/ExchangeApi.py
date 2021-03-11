from abc import ABC, abstractmethod

from services.algorithmic_trading.src.main.exchange.ExchangeService import ExchangeService


class ExchangeApi(ExchangeService, ABC):

    def __init__(self, exchange_name: str, cash_currency: str, crypto_currency: str):
        super().__init__(exchange_name, cash_currency, crypto_currency)

    @abstractmethod
    def execute_sell_order(self, price: float, quantity: float) -> str: pass

    @abstractmethod
    def execute_buy_order(self, price: float, quantity: float) -> str: pass

    @abstractmethod
    def get_account_cash_value(self) -> float: pass

    @abstractmethod
    def get_account_quantity(self) -> float: pass

    @abstractmethod
    def get_order_status(self, order_id: str) -> bool: pass

    @abstractmethod
    def get_open_orders(self) -> list: pass

    @abstractmethod
    def get_transaction_fee(self, order_id: str) -> float: pass

    @abstractmethod
    def get_transactions(self) -> dict: pass

    @abstractmethod
    def get_accrued_account_fees(self) -> float: pass

    @abstractmethod
    def get_successful_cycles(self) -> int: pass

    @abstractmethod
    def get_successful_trades(self) -> int: pass

    @abstractmethod
    def is_order_successful(self, order_id: str) -> bool: pass

    @abstractmethod
    def is_order_status_open(self, order_id: str) -> bool: pass
