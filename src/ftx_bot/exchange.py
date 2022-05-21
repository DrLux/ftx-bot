import time
import hmac
from requests import Request
import pandas as pd
import requests
from order import Order


class Exchange():
    def __init__(self,client) -> None:
        self.client = client   

    def get_single_market(self, market_name):
        return self.client.get_single_market(market_name)

    def get_markets(self):
        return self.client.get_all_markets()

    def get_all_open_orders(self):
        return self.client.get_all_open_orders()

    def get_open_order(self, order_id, market=None):
        return self.client.get_open_order(order_id,market)

    def get_all_wallets(self):
        return self.client.get_all_wallets()

    def get_sub_wallet(self,subwallet):
        return self.client.get_sub_wallet(subwallet)

    def cancel_order(self,order_id):
        return self.client.cancel_order(order_id)
        
    def make_order(self,market,side,price,size,client_id):
        #order = Order()
        return self.client.place_order(market,side,price,size,client_id)

