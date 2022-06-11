from tradingbot.clients.ftx_client import FtxClient
from tradingbot.order import Order,MarketOrder
from tradingbot.order import stopLossLimit  as StopLoss
from tradingbot.clients.ftx_client import FtxClient
from tradingbot.exchange import Exchange
import time 


cfg = {
  "key"                 :  "NISaDMXmmzP64gfq1l2CJ2UjURl-ffm-qAHMsiYs",
  "secret"              :  "El1ZKSgz6jerH_EFZm7ranc-CTyOcj_BmrSWAO6j",
  "subaccount_name"     :  "gold"
}

client = FtxClient(cfg['key'],cfg['secret'],cfg['subaccount_name'])
exchange = Exchange(client)
side = "sell"

print(client._get("orders/history?", {"market":"BTC/USD"})[0])
print(client._get("orders/152246396125"))

'''
marketOrderData = {
    "market"        :   f"BTC/USD",
    "side"          :   side,
    "size"          :   0.0156,
    "price"         :   29859,
    "orderPrice"    :   29860,
    'exchange'      :   exchange
}

text_order = f"Tring to {side} order: {marketOrderData}" 
print(text_order) 
#self.notifier.send_message(text_order)
try:
    order = StopLoss(**marketOrderData)

    while True:
        time.sleep(5)
        print(order.order_info)
        print("############\n")

    
    #if not self.dbManager is None:
    #    self.dbManager.insert_order(order.order_info)
    #    self.dbManager.printAll()
except:
    print("Error during order placement") 
'''


'''
old

{'id': 211919318, 'market': 'BTC/USD', 'future': None, 'side': 'sell', 'type': 'stop', 'orderPrice': 29843.0, 'triggerPrice': 29842.0, 'size': 0.0156, 'status': 'open', 'createdAt': '2022-06-05T21:35:03.744489+00:00', 'triggeredAt': None, 'orderId': None, 'error': None, 'reduceOnly': False, 'trailValue': None, 'trailStart': None, 'cancelledAt': None, 'cancelReason': None, 'retryUntilFilled': False, 'orderType': 'limit'}
{'id': 152245976038, 'clientId': None, 'market': 'BTC/USD', 'type': 'limit', 'side': 'sell', 'price': 29846.0, 'size': 0.0009, 'status': 'closed', 'filledSize': 0.0, 'remainingSize': 0.0, 'reduceOnly': False, 'liquidation': False, 'avgFillPrice': None, 'postOnly': False, 'ioc': False, 'createdAt': '2022-06-05T21:34:49.314682+00:00', 'future': None}
############


nuovo:
{'id': 211921100, 'market': 'BTC/USD', 'future': None, 'side': 'sell', 'type': 'stop', 'orderPrice': 29860.0, 'triggerPrice': 29859.0, 'size': 0.0156, 'status': 'open', 'createdAt': '2022-06-05T21:38:25.124094+00:00', 'triggeredAt': None, 'orderId': None, 'error': None, 'reduceOnly': False, 'trailValue': None, 'trailStart': None, 'cancelledAt': None, 'cancelReason': None, 'retryUntilFilled': False, 'orderType': 'limit'}
{'id': 152246396125, 'clientId': None, 'market': 'BTC/USD', 'type': 'limit', 'side': 'sell', 'price': 29860.0, 'size': 0.0009, 'status': 'closed', 'filledSize': 0.0009, 'remainingSize': 0.0, 'reduceOnly': False, 'liquidation': False, 'avgFillPrice': 29860.0, 'postOnly': False, 'ioc': False, 'createdAt': '2022-06-05T21:38:35.036296+00:00', 'future': None}
############
'''