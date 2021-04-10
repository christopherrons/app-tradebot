import base64
import hashlib
import hmac
import time
import urllib
from urllib import parse

import requests

_API_URL = 'https://api.kraken.com'


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

    def call(self, headers, data):
        # Form request
        url = _API_URL + self.url
        if self.method == 'get':
            response = requests.get(url, headers=headers, data=data).json()
        else:
            response = requests.post(url, headers=headers, data=data).json()
        if isinstance(response, dict) and 'error' in response and response['error'] != []:
            raise APIError(response['error'])
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
        return int(time.time() * 1e6)

    def call(self, **params):
        params.update({'nonce': self.get_nonce()})
        data = params
        post_data = urllib.parse.urlencode(data)

        # Unicode-objects must be encoded before hashing
        encoded = (str(data['nonce']) + post_data).encode()
        message = self.url.encode() + hashlib.sha256(encoded).digest()

        signature = hmac.new(base64.b64decode(self.api_secret),
                             message, hashlib.sha512)
        signature_digest = base64.b64encode(signature.digest())
        headers = {
            'API-Key': self.api_key,
            'API-Sign': signature_digest.decode()
        }
        return super(APIAuthMixin, self).call(headers, data)


class APIOpenOrdersCall(APIAuthMixin):
    url = '/0/private/OpenOrders'


class APIBalanceCall(APIAuthMixin):
    url = '/0/private/Balance'


class APIAccountCash(APIBalanceCall):
    def _process_response(self, response):
        return response['result']


class APIAccountQuantity(APIBalanceCall):
    def _process_response(self, response):
        return response['result']


class APILimitOrder(APIAuthMixin):
    url = '/0/private/AddOrder'


class APIBuyLimitOrder(APILimitOrder):
    def _process_response(self, response):
        print(response)
        return response['result']['txid'][0]


class APISellLimitOrder(APILimitOrder):
    def _process_response(self, response):
        print(response)
        return response['result']['txid'][0]


class APIOpenOrders(APIAuthMixin):
    url = '/0/private/OpenOrders'

    def _process_response(self, response):
        return response['result']


class APIQueryOrders(APIAuthMixin):
    url = '/0/private/QueryOrders'


class APIOrderStatus(APIQueryOrders):
    def _process_response(self, response):
        return list(response['result'].values())[0]['status']


class APIOrderCancelReason(APIQueryOrders):
    def _process_response(self, response):
        return list(response['result'].values())[0]['reason']


class APITransactionFee(APIQueryOrders):
    def _process_response(self, response):
        return list(response['result'].values())[0]['fee']


class APIClosedOrders(APIAuthMixin):
    url = '/0/private/ClosedOrders'

    def _process_response(self, response):
        return response['result']['closed']
