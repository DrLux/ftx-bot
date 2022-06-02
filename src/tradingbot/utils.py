import yaml
from pathlib import Path
import pandas as pd
import requests

class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class DonwloaderCandles(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.resolutions = {
                            "MINUTE": 60,
                            "HOUR"  : 60*60,
                            "DAY"   : 60*60*24,
                            "WEEK"  : 60*60*24*7
                       }    

    def get_resolutions(self):
        return self.resolutions.keys()

    def get_data(self,start,market,resolution=None):
        if resolution is None:
            resolution = self.resolutions["WEEK"]

        start = str(start)
        url = f"https://ftx.com/api/markets/{market}/candles?resolution={resolution}&start_time={start}"
        res = requests.get(url).json()
        df = pd.DataFrame(res['result'])
        df['date'] = pd.to_datetime(df['startTime'])
        df = df.set_index('date')
        rel_df = df.drop(columns=['startTime', 'time','volume'])
        return rel_df



def isBullish(candle):
    lastDiff = candle.close - candle.open 
    isBullish = lastDiff > 0
    return isBullish

'''
params = {
    "prm_dict" : {
        'prova' : 1,
        "sub1": ["primo","secondo"]
    },
    "sec_dict" : {
        'prova' : 2,
        "sub1": "secondo"
    }
}

path = Path("../../parameters/default.yaml")

with path.open('w') as fp:
    yaml.dump(params, fp)
'''