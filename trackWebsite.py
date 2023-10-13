from urllib.parse import urlparse
import requests
from database import Database

class TrackWebsite(): # Controller(or Boundary?)
    def __init__(self):
        self.database = Database()
        self.database.connect()
        
    def __del__(self):
        pass
    
    def enterWebsite(self):
        # Needs a url
        url = ''
        WebsiteDoesNotExist = True
        while WebsiteDoesNotExist:
            url = input("Enter url\nExample: https://google.com\nURL: ")
            # parsedUrl = urlparse(url)
            
            #SPECIAL THANKS TO Adem Öztaş from Stack Overflow
            response = requests.get(url)
            if response.status_code == 200:
                print('Web site exists')
                WebsiteDoesNotExist = False
            else:
                print('Web site does not exist') 
                WebsiteDoesNotExist = True
            
        dict = {"url":url}
        
        self.database.insertPost(dict)
        print("inserted\n", url, "\nsuccessfully")

track = TrackWebsite()
track.enterWebsite()
