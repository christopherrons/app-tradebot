import requests


class CurrencyConverter:
    def __init__(self):
        self.url = 'https://api.exchangeratesapi.io/latest'

    def convert_currency(self, value, from_currency, to_currency):
        latest_rates_in_eur = requests.get(self.url).json()['rates']
        if from_currency.upper() != 'EUR' and to_currency.upper() != 'EUR':
            return (value / latest_rates_in_eur[from_currency.upper()]) * latest_rates_in_eur[
                to_currency.upper()]
        elif to_currency.upper() == 'EUR':
            return value / latest_rates_in_eur[from_currency.upper()]
        else:
            return value * latest_rates_in_eur[to_currency.upper()]
