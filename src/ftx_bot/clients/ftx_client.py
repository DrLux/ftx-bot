import time
import urllib.parse
from typing import Optional, Dict, Any, List
from requests import Request, Session, Response
import hmac
import pandas as pd


# Thanks to https://github.com/ftexchange/ftx

class FtxClient:
    _ENDPOINT = 'https://ftx.com/api/'

    def __init__(self, api_key=None, api_secret=None, subaccount_name=None) -> None:
        self._session = Session()
        self._api_key = api_key
        self._api_secret = api_secret
        self._subaccount_name = subaccount_name
        
    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('GET', path, params=params)
    
    def _post(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('POST', path, json=params)

    def _request(self, method: str, path: str, **kwargs) -> Any:
        request = Request(method, self._ENDPOINT + path, **kwargs)
        self._sign_request(request)
        response = self._session.send(request.prepare())
        return self._process_response(response)

    def _sign_request(self, request: Request) -> None:
        ts = int(time.time() * 1000)
        prepared = request.prepare()
        signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
        if prepared.body:
            signature_payload += prepared.body
        signature = hmac.new(self._api_secret.encode(), signature_payload, 'sha256').hexdigest()
        request.headers['FTX-KEY'] = self._api_key
        request.headers['FTX-SIGN'] = signature
        request.headers['FTX-TS'] = str(ts)
        if self._subaccount_name:
            request.headers['FTX-SUBACCOUNT'] = urllib.parse.quote(self._subaccount_name)

    def _process_response(self, response: Response) -> Any:
        try:
            data = response.json()
        except ValueError:
            response.raise_for_status()
            raise
        else:
            if not data['success']:
                raise Exception(data['error'])
            return data['result']
        
    def place_order(self, market: str, side: str, price: float, size: float, client_id: str,
                    type: str = 'limit', reduce_only: bool = False, ioc: bool = False, post_only: bool = False,
                    ) -> dict:
        return self._post('orders', {'market': market,
                                     'side': side,
                                     'price': price,
                                     'size': size,
                                     'type': type,
                                     'reduceOnly': reduce_only,
                                     'ioc': ioc,
                                     'postOnly': post_only,
                                     'clientId': client_id,
                                     })
    
    def get_open_order(self, order_id: int, market: str = None):
        orders = self._get(f'orders', {'market': market, 'order_id':order_id})
        df = pd.DataFrame(orders)
        df = df.set_index('id')#.T
        return df

    def get_all_open_orders(self):
        orders = self._get("orders")
        df = pd.DataFrame(orders)
        df = df.set_index('id')#.T
        return df 

    def get_all_markets(self):
        markets = self._get('markets')
        df = pd.DataFrame(markets)
        df = df.set_index('name')#.T
        return df

    def get_single_market(self,market_name):
        market_name = market_name.upper()
        market = self._get(f"markets/{market_name}")
        df = pd.DataFrame([market])
        df = df.set_index('name')
        return df

    def get_wallet(self):
        wallet = self._get(f"wallet/balances")
        df = pd.DataFrame(wallet)
        df = df.set_index('coin')
        df = df[df["total"] > 0]
        return df
