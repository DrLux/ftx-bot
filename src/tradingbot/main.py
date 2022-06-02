import hydra
from omegaconf import DictConfig,OmegaConf
from hydra.utils import get_original_cwd
from clients.ftx_client import FtxClient
from exchange import Exchange
from wallet import Wallet
import logging
from order import Order,stopLossLimit,MarketOrder

# A logger for this file
log = logging.getLogger(__name__)

class Bot():
    def __init__(self,cfg) -> None:
        client = FtxClient(cfg.ftx_client['key'],cfg.ftx_client['secret'],cfg.ftx_client['subaccount_name'])
        self.exchange = Exchange(client)
        wallet = Wallet(self.exchange)
        subAccountName = cfg.ftx_client['subaccount_name']
        self.useShadowOrders = cfg.ftx_client['useShadowOrders']
        self.subWallet = wallet.subWallets[subAccountName]
        self.default_fiat = "USD"
        self.mkt_dst = cfg.ftx_client['destination_market'].upper()

    @property
    def isFullFiat(self):
        isfullfiat = self.default_fiat == self.get_wallet_dominance() 
        log.info(f"The wallet is full of Fiat -> {isfullfiat}") 
        return  isfullfiat

    
    def get_wallet_dominance(self):
        balance = self.subWallet.balance
        dom = max(balance, key=balance.get)
        log.info(f"The wallet dominance is {dom} with  {balance[dom]}") 
        return dom

    def run(self):
        if self.isFullFiat:
            self.buyAll()
            self.full_fiat = False
        else:
            self.sellAll()
            self.full_fiat = True

    def buyAll(self):
        size = self.getAllBuyableCoins()
        self.marketOrder("buy",size)
      

    def sellAll(self):
        size = self.getAllSellableCoins()
        self.marketOrder("sell",size)
    

    def getAllSellableCoins(self):
        available_coins = self.subWallet.balance[self.mkt_dst] 
        #print("available_coins: ", available_coins)
        #size = self.exchange.get_change(available_coins,self.mkt_dst,"USD")
        #print("size: ", size)
        return available_coins

    def getAllBuyableCoins(self):
        available_fiat = self.subWallet.balance[self.default_fiat] 
        size = self.exchange.get_change(available_fiat,"USD",self.mkt_dst)
        return size


    def marketOrder(self,side,size):
        marketOrderData = {
            "market": f"{self.mkt_dst}/{self.default_fiat}",
            "side":side,
            "size":size,
            "price":None,
            'exchange':self.exchange
        }

        log.info(f"Tring to {side} order: {marketOrderData}") 
        order = MarketOrder(**marketOrderData)

    '''
    def stopLossLimit(self,price):
        size = self.getAllSellableCoins()
        stopLossLimit = {
            "market": f"{self.mkt_dst}/{self.default_fiat}",
            "side":"sell",
            "size":size,
            "price":price,
            'stopLossPrice': price, 
            'exchange':self.exchange
        }
        order = stopLossLimit(**stopLossLimit)
    '''
    



@hydra.main(version_base=None, config_path='../../parameters', config_name='my_conf.yaml')
def metodo(cfg: DictConfig):
    bot = Bot(cfg)
    bot.run()
   

if __name__ == "__main__":
    metodo()