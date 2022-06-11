import hydra
from omegaconf import DictConfig,OmegaConf,open_dict
from hydra.utils import get_original_cwd
#from bot import Bot
from strategy import Strategy
from tradingbot.notifier import Notifier
from bot import Bot
from dbmanager import DBOrder


# Printare anche il wallet quando fai un acquisto
@hydra.main(version_base=None, config_path='./parameters', config_name='myheikinAshiObserver.yaml')
def main(cfg: DictConfig):
    #dbManager = DBOrder(cfg.dbOrder)
    dbManager = None

    notifier = None
    
    if cfg.bot.useNotifier:
        notifier = Notifier(cfg.notifier)
    
    with open_dict(cfg):
        cfg.strategy.market_src = cfg.bot.market_src
        cfg.strategy.market_dst = cfg.bot.default_fiat
        confBot                 = OmegaConf.merge(cfg['bot'], cfg['ftx_client'])

    strategy = Strategy(cfg.strategy,notifier)
    strategy.plotHA()
    bot = Bot(confBot,strategy,notifier,dbManager)
    bot.run()
    
if __name__ == "__main__":
    main()