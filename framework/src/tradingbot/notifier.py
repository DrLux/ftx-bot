import requests

class Notifier():
    def __init__(self, cfg) -> None:
        self.user_id    = cfg.user_id 
        self.chat_token = cfg.token
    
    def send_message(self, text):
        send_text = f"https://api.telegram.org/bot{self.chat_token}/sendMessage?chat_id={self.user_id}&parse_mode=Markdown&text={text}"
        response = requests.get(send_text)

    def send_image_from_path(self,path):
        send_photo = f"https://api.telegram.org/bot{self.chat_token}/sendPhoto?chat_id={self.user_id}"
        img = {'photo': open(path, 'rb')}
        requests.post(send_photo, files=img)

    def send_image_from_bytes(self,bytes):
        send_photo = f"https://api.telegram.org/bot{self.chat_token}/sendPhoto?chat_id={self.user_id}"
        photo = {'photo': bytes}
        requests.post(send_photo, files=photo)

    def send_image_from_url(self,ulr_img):
        send_photo_url = f"https://api.telegram.org/bot{self.chat_token}/sendPhoto?chat_id={self.user_id}&photo={ulr_img}"
        requests.get(send_photo_url)




