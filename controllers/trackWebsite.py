#pip instal requests
import requests
#pip install icecream
from icecream import ic
class TrackWebsite: # Controller
    def __init__(self):
        #self.database = Database()
        #self.database.connect()
        pass
        
    def __del__(self):
        pass
    
    def enterWebsite(self, url):
        
        statuses = {
            200: "Website Available",
            301: "Permanent Redirect",
            302: "Temporary Redirect",
            404: "Not Found",
            500: "Internal Server Error",
            503: "Service Unavailable"
        }
        
        
        try:
            web_response = requests.get(url, auth=('user','pass'))
            url_info = {
                'url':url,
                'status_num':web_response.status_code,
                'status_desc':statuses[web_response.status_code],
                # 'url_json':web_response.json()
            }
            ic(url_info)
            
                

        except:
            url_info = {
                'url':url,
                'status_num':web_response.status_code,
                'status_desc':statuses[web_response.status_code],
                # 'url_json':web_response.json()
            }
            ic(url_info)




website_url = [
        "https://www.google.co.in", 
        "https://www.yahoo.com", 
        "https://www.amazon.co.in", 
        "https://www.pipsnacks.com/404",
        "http://the-internet.herokuapp.com/status_codes/301",
        "http://the-internet.herokuapp.com/status_codes/500"
    ]
x = TrackWebsite()
for url in website_url:
    # x.enterWebsite(i)
    print(x.enterWebsite(url))