from tradingbot.utils import SingletonMeta

class Exchange(metaclass=SingletonMeta):
    def __init__(self,client=None) -> None:
        self.client = client   

    def get_single_market(self,market_src,market_dest):
        jollyMarket = "USD"
        market_src  = market_src.upper()
        market_dest = market_dest.upper()

        if market_src == jollyMarket:
            dst_usd_price = self.client.get_single_market(f"{market_dest}/{jollyMarket}")['last'][0]
            change = 1/dst_usd_price        
        elif market_dest == jollyMarket:
            src_usd_price = self.client.get_single_market(f"{market_src}/{jollyMarket}")['last'][0]
            change = src_usd_price 
        else:
            src_usd_price = self.client.get_single_market(f"{market_src}/{jollyMarket}")['last'][0]
            dst_usd_price = self.client.get_single_market(f"{market_dest}/{jollyMarket}")['last'][0]
            change = (src_usd_price/dst_usd_price)
        return change

    def get_markets(self):
        return self.client.get_all_markets()

    def get_all_open_orders(self):
        return self.client.get_all_open_orders()

    def get_open_order(self, order_id, market=None):
        return self.client.get_open_order(order_id,market)

    def get_all_wallets(self):
        return self.client.get_all_wallets()

    def get_sub_wallet(self,subwallet):
        return self.client.get_sub_wallet(subwallet)

    def cancel_order(self,order_id):
        return self.client.cancel_order(order_id)
        
    def make_order(self,market,side,price,size,client_id=None,type=None):
        return self.client.place_order(market,side,price,size,client_id,type)

    def place_conditional_order(self,market,side,price,size,type,orderPrice):
        return self.client.place_conditional_order(market,side,price,size,type,orderPrice)

    def get_change(self,size,market_src,market_dest):
        return size * self.get_single_market(market_src,market_dest)