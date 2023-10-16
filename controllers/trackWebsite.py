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