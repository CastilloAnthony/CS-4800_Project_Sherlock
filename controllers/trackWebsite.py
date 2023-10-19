#pip instal requests
import requests
#pip install icecream
from icecream import ic
import socket
import time
class TrackWebsite: # Controller
    def __init__(self):
        #self.database = Database()
        #self.database.connect()
        self.statuses = {
            200: "Website Available",
            301: "Permanent Redirect",
            302: "Temporary Redirect",
            404: "Not Found",
            500: "Internal Server Error",
            503: "Service Unavailable",
            999: "Shit's Fucked"
        }
        
    def __del__(self):
        pass
    
    def enterWebsite(self, url):
        # start = time.time()
        # socket.create_connection((object['website'], port))
        # # end = time.time()
        try:
            web_response = requests.get(url)
            url_info = {
                'url':url,
                'status_num':web_response.status_code,
                'status_desc':self.statuses[web_response.status_code],
                # 'latency': end - start,
                # 'url_json':web_response.json()
            }
            ic(url_info)
            return url_info
    
        except:
            web_response = requests.get(url)
            url_info = {
                'url':url,
                'status_num':web_response.status_code,
                'status_desc':self.statuses[web_response.status_code],
                # 'url_json':web_response.json()
            }
            ic(url_info)
            return url_info

    def print(self):
        print('hello')

website_url = [
        "https://www.google.co.in", 
        "https://www.yahoo.com", 
        "https://www.amazon.co.in", 
        "https://www.pipsnacks.com/404",
        "http://the-internet.herokuapp.com/status_codes/301",
        "http://the-internet.herokuapp.com/status_codes/500"
    ]
website_single_url = "https://www.google.co.in"

# x = TrackWebsite()
# def use_all(website_url):
#     for url in website_url:
#         # x.enterWebsite(i)
#         print(x.enterWebsite(url))

# def get_one(website_single_url):
#     print(x.enterWebsite(website_single_url))
    
# Use one of these
# get_one(website_single_url="https://www.google.co.in")
# use_all(website_url=website_url)
