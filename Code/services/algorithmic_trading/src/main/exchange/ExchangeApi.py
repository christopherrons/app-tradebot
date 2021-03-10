from abc import ABC, abstractmethod


class ExchangeApi(ABC):

    @abstractmethod
    def sell_action(self, price: float, quantity: float) -> str: pass

    @abstractmethod
    def buy_action(self, price: float, quantity: float) -> str: pass

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

    @property
    @abstractmethod
    def exchange_name(self) -> str: pass

    @exchange_name.setter
    @abstractmethod
    def exchange_name(self, exchange_name: str): pass

    @property
    @abstractmethod
    def cash_currency(self) -> str: pass

    @cash_currency.setter
    @abstractmethod
    def cash_currency(self, cash_currency: str): pass

    @property
    @abstractmethod
    def crypto_currency(self) -> str: pass

    @crypto_currency.setter
    @abstractmethod
    def crypto_currency(self, crypto_currency): pass

