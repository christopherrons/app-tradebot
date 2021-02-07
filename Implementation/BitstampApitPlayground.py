from TradebotUtils import TradeBotUtils


# Use class for api calls after testing is done
class BitstampApiPlayground:

    def __init__(self):
        self.bitstamp_token = TradeBotUtils.get_bitstamp_token()

    def get_market_ask_price(self):
        pass

    def get_market_set_price(self):
        pass

    def check_order_status(self):
        pass

    def sell_action(self):
        pass

    def buy_action(self):
        pass
