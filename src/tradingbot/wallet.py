import pandas as pd
from tradingbot.exchange import Exchange
import logging

# A logger for this file
log = logging.getLogger(__name__)

class SubWallet():
    def __init__(self,name,data) -> None:
        self.name           = name 
        self.data           = data
        self.balance        = self.get_balance()
        self.balanceInUsd   = self.get_usd_balance()
        
    @property
    def coins(self):
        return list(self.data.index)

    @property
    def totalUsdValue(self):
        total = self.data.sum(axis = 0, skipna = True)
        return total['usdValue'] 

    def get_usd_balance(self):
        balance = dict()
        for index, row in self.data.iterrows():            
            if row.usdValue > 1:
                balance[index] = row.usdValue
        return balance

    def get_balance(self):
        balance = dict()
        for index, row in self.data.iterrows():            
            balance[index] = row.free
        return balance
    
    def __str__(self):
        return str(self.balance)

    def usd_balance(self):
        usd_balance = dict()
        for index, row in self.data.iterrows():            
            usd_balance[index] = row.usdValue
        return usd_balance


class Wallet():
    def __init__(self,exchange) -> None:
        self.exchange = exchange
        self.subWallets = dict()
        self.syncronize()


    def syncronize(self):
        df = self.exchange.get_all_wallets()
        subWalletNames = list(df.index) 
        
        df = df.T
        for name in subWalletNames:
            balance = self.exchange.get_sub_wallet(name)
            subWallet = SubWallet(name,balance)
            self.subWallets[name] = subWallet

    @property
    def totalUsdValue(self):
        total = 0
        for name,wallet in self.subWallets.items():
            total += wallet.totalUsdValue
        return total

    @property
    def coins(self):
        coins = set()
        for name,wallet in self.subWallets.items():
            coins = coins.union(wallet.coins)
        return coins

