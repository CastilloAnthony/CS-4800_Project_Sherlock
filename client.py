import json # For transferring data between server and client
import multiprocessing # For concurrent processing (interface handling, generation of graphs, etc.)
from database import Database

class ConnectionAgent():
    def __init__(self):
        pass

    def __del__(self):
        pass
#end ConnectionAgent

class Homepage(): # Controller(or Boundary?)
    def __init__(self):
        self.database = Database()

    def __del__(self):
        pass

    def trackWebsite(self):
        pass

    def deleteWebsite(self):
        pass

    def addPreset(self):
        pass

    def editPreset(self):
        pass

    def deletePreset(self):
        pass
#end Homepage

class TrackWebsite(): # Controller(or Boundary?)
    def __init__(self):
        self.database = Database()
        self.database.connect()
        
    def __del__(self):
        pass
    
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
        
        self.database.insertPost(dict)
#end TrackWebsite

class EditPreset(): # Controller(or Boundary?)
    def __init__(self):
        pass

    def __del__(self):
        pass
#end EditPreset

