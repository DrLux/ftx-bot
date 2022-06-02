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

@hydra.main(version_base=None, config_path='../../parameters', config_name='my_conf.yaml')
def metodo(cfg: DictConfig):
    client = FtxClient(cfg.ftx_client['key'],cfg.ftx_client['secret'],cfg.ftx_client['subaccount_name'])
    exchange = Exchange(client)
    subWalletName = 'gold'
    
    print(exchange.get_change(1,"BTC","ETH"))

    '''
    wallet = Wallet(exchange)
    subWallet = wallet.subWallets[subWalletName]
    btc_size = subWallet.balance['USD'] 
    btc_size -= 0.2 

    orderData = {
        "market":"BTC/USD",
        "side":"buy",
        "size":1,
        "price":None,
        "use_shadow":False,
        'exchange':exchange
    }
    order = MarketOrder(**orderData)
    #order.place_order()
    '''


    

if __name__ == "__main__":
    metodo()