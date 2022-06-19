#import plotly
#import plotly.graph_objects as go
from pathlib import Path
from PIL import Image
import io
import mplfinance as mpf


class MPL_Plotter():
    def __init__(self, data) -> None:
        self.data = data
        self.candlestick = data

    # add volume if it present in data
    def plot(self,title,mavs=[],subplots=[]):
        self.create_plot(None,title,mavs,subplots)
 

    def create_plot(self,destination,title=None,mavs=[],subplots=[]):
        #subplot = [    
        #    mpf.make_addplot(df_trades['Trades']),
        #    mpf.make_addplot(df_sell['Sell'],type='scatter',markersize=200,marker='v',color='red'),
        #    mpf.make_addplot(df_buy['Buy'],type='scatter',markersize=200,marker='^',color='green'),
        #]
        plot_volume = "volume" in self.data.columns
        if destination is None:
            mpf.plot(
                        self.data, 
                        title=title,
                        figscale=1.2,
                        figratio=(10, 6),
                        type="candle", 
                        tight_layout=True, 
                        style="binance",
                        mav=mavs, 
                        addplot=subplots,
                        volume=plot_volume
                    )
        else: 
            mpf.plot(
                        self.data, 
                        title=title,
                        figscale=1.2,
                        figratio=(10, 6),
                        type="candle", 
                        tight_layout=True, 
                        style="binance",
                        mav=mavs, 
                        savefig=destination,
                        addplot=subplots,
                        volume=plot_volume
                    )
        return destination
            



    def get_plot_as_bytes(self,title=None,mavs=[],subplots=[]):
        buf = io.BytesIO()
        buf = self.create_plot(buf,title,mavs,subplots)
        buf.seek(0)
        return buf

    def get_plot_as_img(self,title=None,mavs=[],subplots=[]):
        buf = self.get_plot_as_bytes(title,mavs,subplots)
        image = Image.open(buf)
        return image



    def dump_plot(self,path,title=None,mavs=[],subplots=[]):
        path = Path(path) 
        if title is None:
            title = path.stem
        self.create_plot(path,title,mavs,subplots)
        



'''
class DF_Plotter():
    def __init__(self, data) -> None:
        self.data = data
        self.candlestick = go.Candlestick(
                                x     = data.index,
                                open  = data.open,
                                high  = data.high,
                                low   = data.low,
                                close = data.close
                            )
                            
    def create_plot(self,title):
        ATL = self.data['low'].min()
        ATH = self.data['high'].max()

        fig1 = go.Figure(data=[self.candlestick])
        fig1.update_layout(yaxis_range = [ATL,ATH], 
                title = title, 
                xaxis_title = 'Date', 
                yaxis_title = 'Price')
        return fig1

    def plot(self,title):
        fig = self.create_plot(title)
        fig.show()

    def get_plot_as_img(self,title):
        in_memory_file = self.get_plot_as_bytes(title)
        image = Image.open(in_memory_file)
        return image
        
    def get_plot_as_bytes(self,title):
        fig = self.create_plot(title)
        in_memory_file = io.BytesIO()
        plotly.io.write_image(fig, in_memory_file, format='png')
        return in_memory_file


    def dump_plot(self,path,title=None):
        path = Path(path) 
        if title is None:
            title = path.stem
        fig = self.create_plot(title)
        fig.write_image(path)
'''
