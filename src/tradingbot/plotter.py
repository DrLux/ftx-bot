from pathlib import Path
import plotly.graph_objects as go
from PIL import Image
import io

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

    def dump_plot(self,path,title=None):
        path = Path(path) 
        if title is None:
            title = path.stem
        fig = self.create_plot(title)
        fig.write_image(path)

'''
fig = go.Figure(data=[go.Candlestick(x = historical.index,
                                    open = historical['open'],
                                    high = historical['high'],
                                    low = historical['low'],
                                    close = historical['close'],
                                    ),
                     go.Scatter(x=historical.index, y=historical['20 SMA'], line=dict(color='purple', width=1))])


fig.show()
'''