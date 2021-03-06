import hashlib
import hmac
import time

import requests

_API_URL = 'https://api.kraken.com/0/'


class APIError(Exception):
    pass


class APIMixin(object):
    url = None
    method = 'get'

    def _process_response(self, response):
        """
        Allows customized response to be returned.
        """
        return

    def call(self, **params):
        # Form request
        url = _API_URL + self.url
        if self.method == 'get':
            response = requests.get(url, params=params).json()
        else:
            response = requests.post(url, data=params).json()

        if isinstance(response, dict) and 'status' in response and response['status'] == 'error':
            raise APIError(response['reason'])
        new_response = self._process_response(response)
        if new_response is not None:
            response = new_response
        return response


class APIAuthMixin(APIMixin):
    method = 'post'

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def get_nonce(self):
        return bytes(str(int(time.time() * 1e6)), 'utf-8')

    def call(self, **params):
        nonce = self.get_nonce()
        message = nonce + self.api_key
        signature = hmac.new(
            self.api_secret,
            msg=message,
            digestmod=hashlib.sha256).hexdigest().upper()
        params.update({
            'key': self.api_key, 'signature': signature, 'nonce': nonce
        })
        return super(APIAuthMixin, self).call(**params)


# TODO CHeck urls
class APIOpenOrdersCall(APIAuthMixin):
    url = 'private/OpenOrders'


class APIBalanceCall(APIAuthMixin):
    url = 'private/Balance'


class APIAccountCash(APIBalanceCall):
    def _process_response(self, response):
        return response['usd_balance']


class APIAccountQuantity(APIBalanceCall):
    def _process_response(self, response):
        return response['xrp_available']

class APILimitOrder(APIAuthMixin):
    url = 'private/AddOrder'


class APIBuyLimitOrder(APILimitOrder):

    def _process_response(self, response):
        print(response)
        return response['id']


class APISellLimitOrder(APILimitOrder):

    def _process_response(self, response):
        print(response)
        return response['id']


class APIOpenOrders(APIAuthMixin):
    url = 'private/OpenOrders'


class APIOrderStatus(APIOpenOrders):

    def _process_response(self, response):
        return response['status']


class APITransactionFee(APIOpenOrders):

    def _process_response(self, response):
        return response['transactions'][0]['fee']


class APIUserTransactions(APIAuthMixin):
    url = 'private/ClosedOrders'

    def _process_response(self, response):
        return response
