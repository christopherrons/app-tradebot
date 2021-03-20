class ExchangeService:
    def __init__(self, exchange_name: str, cash_currency: str, crypto_currency: str):
        self._exchange_name = exchange_name
        self._cash_currency = cash_currency
        self._crypto_currency = crypto_currency

    @property
    def exchange_name(self) -> str:
        return self._exchange_name

    @exchange_name.setter
    def exchange_name(self, exchange_name: str):
        self._exchange_name = exchange_name

    @property
    def cash_currency(self) -> str:
        return self._cash_currency

    @cash_currency.setter
    def cash_currency(self, cash_currency: str):
        self._cash_currency = cash_currency

    @property
    def crypto_currency(self) -> str:
        return self._crypto_currency

    @crypto_currency.setter
    def crypto_currency(self, crypto_currency: str):
        self._crypto_currency = crypto_currency
