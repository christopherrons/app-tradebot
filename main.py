class CryptoBot:

    def __init__(self, buy_price, interest, initial_value, is_buy=True):
        self.buy_price = buy_price
        self.interest = interest
        self.sell_price = (1 + interest) * buy_price
        self.initial_value = initial_value
        self.is_buy = is_buy

    def run(self):
        "Runner"
        while True:
            self.trade_decision_algorithm()

    def get_ask_price(self):
        "Gets the current ask price of the crypto currency"

    def get_bid_price(self):
        "Gets the current bid price of the crypto currency"

    def trade_decision_algorithm(self):
        "Decision to buy or sell"
        if self.is_buy:
            if self.buy_price == self.get_ask_price():
                self.trade_action_buy()
        else:
            if self.sell_price == self.get_bid_price():
                self.trade_action_sell()

    def trade_action_buy(self):
        "Http-request to Bistamp API"
        self.is_buy = False

    def trade_action_sell(self):
        "Http-request to Bistamp API"
        self.is_buy = True

    def is_successful_trade(self):
        ""