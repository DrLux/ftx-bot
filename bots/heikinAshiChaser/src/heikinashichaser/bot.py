from tradingbot.clients.ftx_client import FtxClient
from tradingbot.exchange import Exchange
from tradingbot.order import Order,stopLossLimit,MarketOrder
from tradingbot.wallet import Wallet
import logging

# A logger for this file
log = logging.getLogger(__name__)

class Bot():
    ## Togliere il notifier da dentro strategy e metterlo a parte
    ## Nel buyall eliminare il caso in cui prova a comprare pochi cents. Se non ho nulla da comrpare il buy all non si deve triggerare
    def __init__(self,cfg,strategy,notifier=None,dbManager=None) -> None:
        client = FtxClient(cfg['key'],cfg['secret'],cfg['subaccount_name'])
        self.exchange       = Exchange(client)
        wallet              = Wallet(self.exchange)
        self.strategy       = strategy
        subAccountName      = cfg['subaccount_name']
        self.subWallet      = wallet.subWallets[subAccountName]
        self.default_fiat   = cfg['default_fiat']
        self.market_src     = cfg['market_src'].upper()
        self.testMode       = cfg['testMode']
        self.notifier       = notifier
        self.dbManager      = dbManager
        self.init_portfolio()

    @property
    def isFullFiat(self):
        self.full_fiat = self.default_fiat == self.get_wallet_dominance() 
        #log.info(f"The wallet is full of Fiat -> {self.full_fiat}") 
        return  self.full_fiat

    
    def get_wallet_dominance(self):
        balance = self.subWallet.balanceInUsd
        dom = max(balance, key=balance.get)
        log.info(f"The wallet dominance is {dom} with  {balance[dom]}") 
        return dom

    def init_portfolio(self):
        log.info(f"Initializing portfolio. The test mode is {self.testMode}") 
        if not self.testMode:
            isBullish = self.strategy.checkIfBullish()
            fullFiat  = self.isFullFiat
            log.info(f"Flag isBullish = {isBullish} and flag fullFiat = {fullFiat}.") 
            if isBullish and fullFiat:
                log.info(f"Init prortfolio with buyall.") 
                self.buyAll() 
            elif not isBullish and not fullFiat:
                log.info(f"Init prortfolio with sellall.") 
                self.sellAll() 

    def run(self):       
        whatToDo = self.strategy.whatToDo()
        if not self.testMode:
            if whatToDo == "buy":
                self.buyAll()
            elif whatToDo == "sell":
                self.sellAll()
            else:
                print("Do nothing!")


    def buyAll(self):
        if self.full_fiat: 
            log.info(f"Buying all triggered")
            size = self.getAllBuyableCoins()
            self.marketOrder("buy",size)
            self.full_fiat = False
        else:
            log.info(f"Buying all triggered but not executed since full_fiat is {self.full_fiat}")

        

    def sellAll(self):
        if not self.full_fiat: 
            size = self.getAllSellableCoins()
            log.info(f"Selling all triggered. All Sellable Coins: {size}")
            self.marketOrder("sell",size)
            self.full_fiat = True
        else:
            log.info(f"SellAll triggered but not executed since full_fiat is {self.full_fiat}")

    

    def getAllSellableCoins(self):
        available_coins = self.subWallet.balance[self.market_src] 
        return available_coins

    def getAllBuyableCoins(self):
        available_fiat = self.subWallet.balance[self.default_fiat] 
        size = self.exchange.get_change(available_fiat,"USD",self.market_src)
        return size


    def marketOrder(self,side,size):
        marketOrderData = {
            "market": f"{self.market_src}/{self.default_fiat}",
            "side":side,
            "size":size,
            "price":None,
            'exchange':self.exchange
        }

        text_order = f"Tring to {side} order: {marketOrderData}" 
        log.info(text_order) 
        self.notifier.send_message(text_order)
        try:
            order = MarketOrder(**marketOrderData)
            if not self.dbManager is None:
                self.dbManager.insert_order(order.order_info)
                self.dbManager.printAll()
        except:
            log.info("Error during order placement") 
        
        self.strategy.showWallet(self.subWallet.balance)

    '''
    def stopLossLimit(self,price):
        size = self.getAllSellableCoins()
        stopLossLimit = {
            "market": f"{self.market_dst}/{self.default_fiat}",
            "side":"sell",
            "size":size,
            "price":price,
            'stopLossPrice': price, 
            'exchange':self.exchange
        }
        order = stopLossLimit(**stopLossLimit)
    '''
    