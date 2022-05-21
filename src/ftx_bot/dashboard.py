import plotly.graph_objects as go
fig = go.Figure(data=[go.Candlestick(x = historical.index,
                                    open = historical['open'],
                                    high = historical['high'],
                                    low = historical['low'],
                                    close = historical['close'],
                                    ),
                     go.Scatter(x=historical.index, y=historical['20 SMA'], line=dict(color='purple', width=1))])


fig.show()