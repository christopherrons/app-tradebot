from Implementation.Utils.BitstampAPIUtils import APIBuyLimitOrder, APIOrderStatus, APITransactionFee, \
    APIAccountQuantity, APIAccountCash, APISellLimitOrder


class BitstampAPIAction:

    def __init__(self, customer_id, api_key, api_secret):
        self.customer_id = customer_id
        self.api_key = api_key
        self.api_secret = api_secret

    def sell_action(self, price, quantity):
        return APISellLimitOrder(self.customer_id, self.api_key, self.api_secret).call(price=price,
                                                                                       amount=quantity,
                                                                                       fok_order=True)

    def buy_action(self, price, quantity):
        return APIBuyLimitOrder(self.customer_id, self.api_key, self.api_secret).call(price=price,
                                                                                      amount=quantity,
                                                                                      fok_order=True)

    def get_account_cash_value(self):
        return APIAccountCash(self.customer_id, self.api_key, self.api_secret).call()

    def get_account_quantity(self):
        return APIAccountQuantity(self.customer_id, self.api_key, self.api_secret).call()

    def get_position_value(self):
        # xrp_available
        pass

    def get_xrpusd_fee(self):
        pass

    def get_usdxrp_fee(self):
        pass

    def get_order_status(self, order_id):
        return APIOrderStatus(self.customer_id, self.api_key, self.api_secret).call(id=order_id)

    def get_transaction_fee(self):
        return APITransactionFee(self.customer_id, self.api_key, self.api_secret).call(offset=0,
                                                                                       sort='desc',
                                                                                       limit=1)
