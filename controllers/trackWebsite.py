<<<<<<< HEAD
class TrackWebsite(): # Controller
=======
#pip instal requests
import requests
#pip install icecream
from icecream import ic
class TrackWebsite: # Controller
>>>>>>> b6d7d20693893b4f917998e128301f81783596ae
    def __init__(self):
        #self.database = Database()
        #self.database.connect()
        pass
        
    def __del__(self):
        pass
    
<<<<<<< HEAD
    def enterWebsite(self):
        # Needs a url
        prefixList = ["HTTPS://, HTTP://"]
        extensionList = [".COM", 
                         ".NET", 
                         ".ORG", 
                         "BIZ", 
                         ".GOV", 
                         ".INFO", 
                         ".EDU", 
                         ".TV",
                         ]
        
        prefixBool = True
        extensionBool = True
        url = ''
        
        while prefixBool and extensionBool:
            url = input("Enter url\nExample: https://google.com\nURL: ").upper()
            
            print(url)
            for prefix in prefixList:
                if prefix in url: prefixBool = False
            for extension in extensionList:
                if extension in url: extensionBool = False
            else:
                continue
        print(url)
        dict = {"url":url}
        
        #self.database.insertPost(dict)
#end TrackWebsite
=======
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
website_single_url = "https://www.google.co.in"

x = TrackWebsite()
def use_all(website_url):
    for url in website_url:
        # x.enterWebsite(i)
        print(x.enterWebsite(url))

def get_one(website_single_url):
    print(x.enterWebsite(website_single_url))
    
# Use one of these
# get_one(website_single_url="https://www.google.co.in")
# use_all(website_url=website_url)
>>>>>>> b6d7d20693893b4f917998e128301f81783596ae
