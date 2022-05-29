#import telegram_send

class Notifier():
    def __init__(self) -> None:
        pass
    
    def send_message(self, text):
        pass
        #telegram_send.send(messages=[text])

    def send_image_from_file(self,path):
        with open(path, "rb") as f:
            pass
            #telegram_send.send(images=[f])

    def send_image(self,img):
        pass
        #telegram_send.send(images=[img])
