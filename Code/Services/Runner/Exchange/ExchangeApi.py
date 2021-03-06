from abc import ABC, abstractmethod


class ExchangeApi(ABC):

    @abstractmethod
    def sell_action(self, price, quantity): pass

    @abstractmethod
    def buy_action(self, price, quantity): pass

    @abstractmethod
    def get_account_cash_value(self): pass

    @abstractmethod
    def get_account_quantity(self): pass

    @abstractmethod
    def get_order_status(self, order_id): pass

    @abstractmethod
    def get_open_orders(self): pass

    @abstractmethod
    def get_transaction_fee(self, order_id): pass

    @abstractmethod
    def get_transactions(self): pass

    @abstractmethod
    def get_accrued_account_fees(self): pass

    @abstractmethod
    def get_successful_cycles(self): pass

    @abstractmethod
    def get_successful_trades(self): pass

    @abstractmethod
    def is_order_successful(self, order_id): pass

    @abstractmethod
    def is_order_status_open(self, order_id): pass

    @abstractmethod
    def get_exchange_name(self): pass
