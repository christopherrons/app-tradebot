import requests


class CurrencyConverter:
    def __init__(self):
        self.__base_url = 'https://api.frankfurter.app/'
        self.__base_currency = "?base=SEK"

    def convert_currency_from_api(self, value: float, from_currency: str, to_currency: str, date="latest") -> float:
        if from_currency == to_currency:
            return value

        latest_rates_in_sek = requests.get(self.__base_url + date + self.__base_currency).json()['rates']
        if from_currency.upper() != 'SEK' and to_currency.upper() != 'SEK':
            return (value / latest_rates_in_sek[from_currency.upper()]) * latest_rates_in_sek[to_currency.upper()]
        elif to_currency.upper() == 'SEK':
            return value / latest_rates_in_sek[from_currency.upper()]
        else:
            return value * latest_rates_in_sek[to_currency.upper()]

    @staticmethod
    def convert_currency_from_rate(value: float, rate: float) -> float:
        return value * rate
