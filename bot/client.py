from binance.client import Client
import os

class BinanceFuturesClient:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)

        # Testnet URL
        self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

    def place_order(self, **kwargs):
        return self.client.futures_create_order(**kwargs)