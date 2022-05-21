class Order():
    def __init__(self,type,prize,use_shadow=False) -> None:
        self.type = type 
        self.prize = prize 
        self.use_shadow = use_shadow
        self.order_id = None 
        

    def send_notification(self):
        pass 

    def store_order(self):
        pass