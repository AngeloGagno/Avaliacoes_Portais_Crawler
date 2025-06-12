import requests
from datetime import datetime,timedelta

class Portal_Reviews:

    def __init__(self,cookies:dict):
        self.session_cookies = cookies
    
    def request(self):
        request = requests.get(self.url(), cookies=self.session_cookies)
        try:
            return request.json()
        except:
            raise ConnectionError
        
    def url(self):
        return 'https://app.pineapples.com.br/channelmanager-api/v1/' \
    'accommodations?channel=bk_airbnb&limit=1000'