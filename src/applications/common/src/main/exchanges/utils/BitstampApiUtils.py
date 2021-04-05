import hashlib
import hmac
import time

import requests

_API_URL = 'https://www.bitstamp.net/api/'


class APIError(Exception):
    pass


class APIMixin(object):
    url = None
    method = 'get'

    def __init__(self, url):
        self.url = url

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

    def __init__(self, customer_id: bytes, api_key: bytes, api_secret: bytes, url: str):
        self.customer_id = customer_id
        self.api_key = api_key
        self.api_secret = api_secret
        super().__init__(url)

    def get_nonce(self):
        return bytes(str(int(time.time() * 1e6)), 'utf-8')

    def call(self, **params):
        nonce = self.get_nonce()
        message = nonce + self.customer_id + self.api_key
        signature = hmac.new(
            self.api_secret,
            msg=message,
            digestmod=hashlib.sha256).hexdigest().upper()
        params.update({
            'key': self.api_key, 'signature': signature, 'nonce': nonce
        })
        return super(APIAuthMixin, self).call(**params)


class APIAccountCash(APIAuthMixin):
    def _process_response(self, response):
        return response


class APIAccountQuantity(APIAuthMixin):
    def _process_response(self, response):
        return response


class APIBuyLimitOrder(APIAuthMixin):

    def _process_response(self, response):
        print(response)
        return response['id']


class APISellLimitOrder(APIAuthMixin):
    def _process_response(self, response):
        print(response)
        return response['id']


class APIOrderStatus(APIAuthMixin):
    def _process_response(self, response):
        return response['status']


class APIOpenOrders(APIAuthMixin):
    def _process_response(self, response):
        return response


class APITransactionFee(APIAuthMixin):

    def _process_response(self, response):
        return response['transactions'][0]['fee']


class APIUserTransactions(APIAuthMixin):
    def _process_response(self, response):
        return response
