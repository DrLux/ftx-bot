import hydra
from omegaconf import DictConfig,OmegaConf
from hydra.utils import get_original_cwd
from clients.ftx_client import FtxClient
from exchange import Exchange
from wallet import Wallet
import logging
from order import Order,stopLossLimit

# A logger for this file
log = logging.getLogger(__name__)

@hydra.main(version_base=None, config_path='../../parameters', config_name='my_conf.yaml')
def metodo(cfg: DictConfig):
    client = FtxClient(cfg.ftx_client['key'],cfg.ftx_client['secret'],cfg.ftx_client['subaccount_name'])
    exchange = Exchange(client)
    

    import time
    #print("stampa prima: ", exchange.get_all_open_orders())
    #print(r)
    #exchange.cancel_order(148396000502)
    #print("stampa dopo: ", exchange.get_all_open_orders())
    #print(exchange.get_open_order("139563598672"))
    log.info("nel main")
    
    o = stopLossLimit(market="BTC/USD",side="buy",price=31340,size=0.0001)
    o.cancel_order()
    
    
    #o = Order(market="USDT/USD",side="buy",price=0.90,size=1)
    #wallet = exchange.get_sub_wallet('gold')
    #wallet = Wallet()
    #print(wallet.coins)
    #wallet = exchange.get_all_wallets()
    #print("solo gold: \n", wallet)

    

if __name__ == "__main__":
    metodo()