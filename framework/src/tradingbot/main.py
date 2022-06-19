'''
import hydra
from omegaconf import DictConfig,OmegaConf
from hydra.utils import get_original_cwd
from clients.ftx_client import FtxClient
from exchange import Exchange
from wallet import Wallet
import logging
from order import Order,stopLossLimit,MarketOrder
from utils import DonwloaderCandles
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import mplfinance as mpf

# A logger for this file
log = logging.getLogger(__name__)

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + timedelta(days_ahead)

def prepareData(lastMonts,donwloader,market):
    currentDate     = datetime.now()
    #starting the week always from Tuesday, to aling the result to the tradingview's one
    currentDate     = next_weekday(currentDate, 1) # 0 = Monday, 1=Tuesday, 2=Wednesday...

    past_date       = currentDate - relativedelta(months=lastMonts)
    start           = datetime(past_date.year,past_date.month,past_date.day)
    start           = start.timestamp()
    resolution      = donwloader.resolutions
    data            = donwloader.get_data(start,market,resolution['WEEK'])
    data            = data[:-1] # remove last incompleted week
    return data




# GET DATA
donwloader  = DonwloaderCandles()
resolution = donwloader.resolutions
data = prepareData(3,donwloader,"PAXG/USD")
print(data)



#subplot = [    
#    mpf.make_addplot(df_trades['Trades']),
#    mpf.make_addplot(df_sell['Sell'],type='scatter',markersize=200,marker='v',color='red'),
#    mpf.make_addplot(df_buy['Buy'],type='scatter',markersize=200,marker='^',color='green'),
#]
        
link_plot = './cangle_plot.jpg'

plot_volume = "volume" in data.columns
filepath = None 
mavs = []
subplots = []

a = mpf.plot(
            data, 
            title="ciao",
            figscale=1.2,
            figratio=(10, 6),
            type="candle", 
            tight_layout=True, 
            style="binance",
            #savefig=False,
            mav=mavs, 
            addplot=subplots,
            volume=plot_volume
        )

import io
from PIL import Image

buf = io.BytesIO()
mpf.plot(data,type='candle',savefig=buf)
buf.seek(0)
buff_image = buf
image = Image.open(buff_image)
image.show()
'''