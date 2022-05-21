import hydra
from omegaconf import DictConfig,OmegaConf
from hydra.utils import get_original_cwd
from clients.ftx_client import FtxClient
from exchange import Exchange


@hydra.main(version_base=None, config_path='../../parameters', config_name='my_conf.yaml')
def metodo(cfg: DictConfig):
    print(OmegaConf.to_yaml(cfg))
    client = FtxClient(cfg.ftx_client['key'],cfg.ftx_client['secret'])
    
    exchange = Exchange(client)
    #orders = exchange.get_open_order(147591862447,"BTC/USD")
    wallet = exchange.get_wallet()
    print(wallet)

if __name__ == "__main__":
    metodo()