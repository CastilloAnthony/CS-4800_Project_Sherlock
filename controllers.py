#CONTROLLERS
#CONTROLLERS
#CONTROLLERS
import multiprocessing # For concurrent processing (interface handling, generation of graphs, etc.)
#from database import Database 

# ALL OF THESE RETURN TO CLIENT

class Homepage(): # Controller
    def __init__(self):
        #self.database = Database()
        self.__trackWebsite = TrackWebsite() # Controller
        self.__deleteWebsite = DeleteWebsite() # Controller
        self.__addPreset = AddPreset() # Controller
        self.__editPreset = EditPreset() # Controller
        self.__deletePreset = DeletePreset() # Controller

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

class TrackWebsite(): # Controller
    def __init__(self):
        #self.database = Database()
        #self.database.connect()
        pass
        
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
        
        #self.database.insertPost(dict)
#end TrackWebsite

class DeleteWebsite(): # Controller
    def __init__(self):
        pass

    def __del__(self):
        pass
#end DeleteWebsite

class AddPreset(): # Controller
    def __init__(self):
        pass

    def __del__(self):
        pass
#end AddPreset

class EditPreset(): # Controller
    def __init__(self):
        pass

    def __del__(self):
        pass
#end EditPreset

class DeletePreset(): # Controller
    def __init__(self):
        pass

    def __del__(self):
        pass
#end DeletePreset