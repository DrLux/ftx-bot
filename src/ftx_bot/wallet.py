import pandas as pd

class SubWallet():
    def __init__(self,name,balance) -> None:
        self.name = name 
        self.balance = balance
        
    @property
    def coins(self):
        return list(self.balance.index)

    @property
    def totalUsdValue(self):
        total = self.balance.sum(axis = 0, skipna = True)
        return total['usdValue'] 


class Wallet():
    def __init__(self,exchange=None) -> None:
        self.subWallets = dict()
        if exchange:
            self.exchange = exchange 
            self.syncronize(exchange)


    def syncronize(self,exchange):
        df = exchange.get_all_wallets()
        subWalletNames = list(df.index) 
        
        df = df.T
        for name in subWalletNames:
            balance = exchange.get_sub_wallet(name)
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

