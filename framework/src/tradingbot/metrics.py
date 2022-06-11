import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from tradingbot.utils import isBullish

class HeikinAshi():
    def __init__(self,data) -> None:
        self.data = data 

    def calculate(self):
        #STEP 0:
        #assigning existing columns to new variable HAdf
        #HAdf = rel_df[['OPEN', 'HIGH', 'LOW', 'CLOSE']]
        HAdf = self.data.copy()

        #STEP 1:
        #HAClose = (Open0 + High0 + Low0 + Close0)/4
        #round function to limit results to 2 decimal places
        HAdf['close'] = round(((self.data['open'] + self.data['high'] + self.data['low'] + self.data['close'])/4),2)

        #STEP 2:
        #HAOpen = (HAOpen(-1) + HAClose(-1))/2
        #df.iat[row,col]:  Access a single value for a row/column pair by integer position.
        for i in range(len(self.data)):
            if i == 0:
                HAdf.iat[0,0] = round(((self.data['open'].iloc[0] + self.data['close'].iloc[0])/2),2)
            else:
                HAdf.iat[i,0] = round(((HAdf.iat[i-1,0] + HAdf.iat[i-1,3])/2),2) #0 = OPEN, 3 = CLOSE

        #STEP 3:
        #High = MAX(High0, HAOpen, HAClose)
        #Low = MIN(Low0, HAOpen, HAClose)

        #Taking the Open and Close columns we worked on in Step 2 & 3
        #Joining this data with the existing HIGH/LOW data from rel_df
        #Taking the max value in the new row with columns OPEN, CLOSE, HIGH
        #Assigning that value to the HIGH/LOW column in HAdf

        HAdf['high'] = HAdf.loc[:,['open', 'close']].join(self.data['high']).max(axis=1)
        HAdf['low'] = HAdf.loc[:,['open', 'close']].join(self.data['low']).min(axis=1)

        return HAdf

    def trendChange(self,hadf):
        lastCandle          = isBullish(hadf.iloc[-1]) 
        secondLastCandle    = isBullish(hadf.iloc[-2])
        trendChanged = lastCandle != secondLastCandle      

        return trendChanged
    
        
