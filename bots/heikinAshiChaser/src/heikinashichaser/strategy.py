
from tradingbot.plotter import MPL_Plotter
from tradingbot.utils import DonwloaderCandles,isBullish
from datetime import datetime
from datetime import timedelta

from tradingbot.metrics import HeikinAshi
from dateutil.relativedelta import relativedelta
from pathlib import Path

import logging

# A logger for this file
log = logging.getLogger(__name__)   

class Strategy():
    def __init__(self,cfg,notifier=None) -> None:
        self.lastMonts   = cfg['numMonth']
        self.market      = f"{cfg['market_src']}/{cfg['market_dst']}" 
        self.notifier    = notifier
        self.donwloader  = DonwloaderCandles()

    def next_weekday(self, d, weekday):
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0: # Target day already happened this week
            days_ahead += 7
        return d + timedelta(days_ahead)
        
    def prepareData(self,lastMonts):
        currentDate     = datetime.now()
        #starting the week always from Tuesday, to aling the result to the tradingview's one
        currentDate     = self.next_weekday(currentDate, 1) # 0 = Monday, 1=Tuesday, 2=Wednesday...

        past_date       = currentDate - relativedelta(months=lastMonts)
        start           = datetime(past_date.year,past_date.month,past_date.day)
        start           = start.timestamp()
        resolution = self.donwloader.resolutions
        data = self.donwloader.get_data(start,self.market,resolution['WEEK'])
        data = data[:-1] # remove last incompleted week
        return data
        

    def calculate(self):
        data = self.prepareData(self.lastMonts)
        ha = HeikinAshi(data)
        hadf = ha.calculate()        
        return ha,hadf

    def plotHA(self):
        ha,hadf = self.calculate()
        #plotter = DF_Plotter(hadf[-10:])
        plotter = MPL_Plotter(hadf[:])
        title = f"The HeikinAshi plot for market [{self.market}]!"
        plotter.plot(title)       


    def sendNotification(self,hadf,trendChanged,bullish,whatToDO):
        currentDate     = datetime.now()
        currend_date    = currentDate.strftime("%D:%M:%Y")  
        plotter = MPL_Plotter(hadf[-10:])       

        # SEND PLOT BULLISH/BEARISH        
        if bullish:
            title = f"In [{currend_date}] the market [{self.market}] is BULLISH!"
        else:
            title = f"In [{currend_date}] the market [{self.market}] is BEARISHI!"
        plot_img = plotter.get_plot_as_bytes(title)
        self.notifier.send_image_from_bytes(plot_img.getbuffer())
        
        # Trend Changed
        if trendChanged:
            self.notifier.send_message(f"The trend is changed!")        
        else:
            self.notifier.send_message(f"The trend is NOT changed!")        

        self.notifier.send_message(f" You should {whatToDO}")    

    def showWallet(self,balance):
        self.notifier.send_message(f" Now your waller is {balance}")    
        

    def checkIfBullish(self):
        ha,hadf = self.calculate()
        bullFlag = isBullish(hadf.iloc[-1])
        log.info(f"The bullflag is {bullFlag} since the last candle is {hadf.iloc[-1]}") 
        return bullFlag


    def whatToDo(self):
        ha,hadf = self.calculate()
        log.info(f"Calculate the HeikinAshi") 

        trendChanged = ha.trendChange(hadf)
        log.info(f"The trend is changed -> {trendChanged}") 

        bullish = isBullish(hadf.iloc[-1])
        log.info(f"The plot is bullish -> {bullish}") 
        
        if trendChanged and bullish:
            whatToDO = "buy"
        elif trendChanged and not bullish:
            whatToDO = "sell"
        else:
            whatToDO = "wait"
        log.info(f"You should -> {whatToDO}") 

        if not self.notifier is None:
            self.sendNotification(hadf,trendChanged,bullish,whatToDO)
        
        return whatToDO

      
