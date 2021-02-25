import requests
import hmac
import hashlib
import time

_API_URL = 'https://www.bitstamp.net/api/'


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

    def __init__(self, customer_id, api_key, api_secret):
        self.customer_id = customer_id
        self.api_key = api_key
        self.api_secret = api_secret

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

#TODO CHeck urls
class APIOpenOrdersCall(APIAuthMixin):
    url = 'v2/open_orders/'


class APIBalanceCall(APIAuthMixin):
    url = 'v2/balance/'


class APIAccountCash(APIBalanceCall):
    def _process_response(self, response):
        return response['usd_balance']


class APIAccountQuantity(APIBalanceCall):
    def _process_response(self, response):
        return response['xrp_available']


class APIBuyLimitOrder(APIAuthMixin):
    url = 'v2/buy/xrpusd/'

    def _process_response(self, response):
        print(response)
        return response['id']


class APISellLimitOrder(APIAuthMixin):
    url = 'v2/sell/xrpusd/'

    def _process_response(self, response):
        print(response)
        return response['id']


class APIOrderStatus(APIAuthMixin):
    url = 'v2/order_status/'

    def _process_response(self, response):
        return response['status']


class APIOpenOrders(APIAuthMixin):
    url = 'v2/open_orders/all/'

    def _process_response(self, response):
        return response


class APITransactionFee(APIAuthMixin):
    url = 'v2/user_transactions/'

    def _process_response(self, response):
        return response[0]['fee']
