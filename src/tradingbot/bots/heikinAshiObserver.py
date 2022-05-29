
from tradingbot.plotter import DF_Plotter
from tradingbot.utils import DonwloaderCandles,isBullish
from datetime import datetime

import hydra
from omegaconf import DictConfig,OmegaConf
from tradingbot.metrics import HeikinAshi
from tradingbot.exchange import Exchange
from tradingbot.notifier import Notifier
from dateutil.relativedelta import relativedelta
from pathlib import Path

import logging

# A logger for this file
log = logging.getLogger(__name__)



@hydra.main(version_base=None, config_path='../../../parameters', config_name='heikinAshiObserver.yaml')
def main(cfg: DictConfig):
    currentDate     = datetime.now()
    lastMonts       = cfg['numMonth']

    donwloader = DonwloaderCandles()
    past_date = currentDate - relativedelta(months=lastMonts)
    notifier = Notifier()


    start   = datetime(past_date.year,past_date.month,past_date.day)
    start   = start.timestamp()
    markets = cfg['markets'] 



    for market in markets:
        df = donwloader.get_data(start,market)
        ha = HeikinAshi(df)
        hadf = ha.calculate()
        
        temp_path = Path("./temp.jpg")
    
        plotter = DF_Plotter(hadf)

        buyFlag = isBullish(hadf)
        
        currend_date = currentDate.strftime("%D:%M:%Y")
        if buyFlag:
            title = f"{currend_date} {market} is Bullish"
        else:
            title = f"In [{currend_date}] the market [{market}] is Bearish!"
        
        plotter.dump_plot(str(temp_path),title=title)
        #notifier.send_image_from_file(str(temp_path))
        notifier.send_message(f"Last candle for {market} is: {df.iloc[-1]}")
        temp_path.unlink()

    notifier.send_message("###########################################")
    

if __name__ == "__main__":
    main()