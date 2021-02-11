import asyncio
import websockets
import json
import ast


class BitstampApiAction:

    def __init__(self, bitstamp_token, market):
        self.__bitstamp_token = bitstamp_token
        self.__uri = "wss://ws.bitstamp.net/"
        self.__subscription = {
            "event": "bts:subscribe",
            "data": {
                "channel": f"order_book_{market}"
            }
        }
        self.current_order_id = None

    def get_market_ask_price_and_quantity(self):
        return asyncio.get_event_loop().run_until_complete(self.async_get_market_ask_price_and_quantity())

    async def async_get_market_ask_price_and_quantity(self):

        async with websockets.connect(self.__uri) as websocket:
            await websocket.send(json.dumps(self.__subscription))

            data = ast.literal_eval(await websocket.recv())
            while data['data'] == {}:
                data = ast.literal_eval(await websocket.recv())

            market_ask_price = float(data['data']['asks'][0][0])
            market_ask_quantity = float(data['data']['asks'][0][1])
            return market_ask_price, market_ask_quantity

    def get_market_bid_price_and_quantity(self):
        return asyncio.get_event_loop().run_until_complete(self.async_get_market_bid_price_and_quantity())

    async def async_get_market_bid_price_and_quantity(self):

        async with websockets.connect(self.__uri) as websocket:
            await websocket.send(json.dumps(self.__subscription))

            data = ast.literal_eval(await websocket.recv())
            while data['data'] == {}:
                data = ast.literal_eval(await websocket.recv())

            market_bid_price = float(data['data']['bids'][0][0])
            market_bid_quantity = float(data['data']['bids'][0][1])
            return market_bid_price, market_bid_quantity

    def get_market_ask_price(self):
        return asyncio.get_event_loop().run_until_complete(self.async_get_market_ask_price())

    async def async_get_market_ask_price(self):

        async with websockets.connect(self.__uri) as websocket:
            await websocket.send(json.dumps(self.__subscription))

            data = ast.literal_eval(await websocket.recv())
            while data['data'] == {}:
                data = ast.literal_eval(await websocket.recv())

            return float(data['data']['asks'][0][0])

    def get_market_bid_price(self):
        return asyncio.get_event_loop().run_until_complete(self.async_get_market_bid_price())

    async def async_get_market_bid_price(self):

        async with websockets.connect(self.__uri) as websocket:
            await websocket.send(json.dumps(self.__subscription))

            data = ast.literal_eval(await websocket.recv())
            while data['data'] == {}:
                data = ast.literal_eval(await websocket.recv())

            return float(data['data']['bids'][0][0])

    def check_order_status(self):
        pass

    def sell_action(self):
        # sell quantity (amount)
        # sell price
        # fok_order = true
        # get order id
        pass

    def buy_action(self):
        # buy quantity (amount)
        # buy price
        # fok_order = true
        # get order id
        pass

    def get_account_quantity(self):
        pass

    def get_account_cash(self):
        # usd_balance
        pass

    def get_position_value(self):
        # xrp_available
        pass

    def get_xrpusd_fee(self):
        # xrpusd
        pass

    def get_usdxrp_fee(self):
        pass

    def get_order_status(self):
        pass

    def get_transascton_fee(self):
        # there is a transaction fee in api
        pass
