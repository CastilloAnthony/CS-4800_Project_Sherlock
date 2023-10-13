# use website: https://www.mongodb.com/try/download/community
# download mongodb version 7.0
import pymongo
class Database:
    def __init__(self):
        self.myclient = False
        self.mydb = False
        self.mycol = False
    
    def connect(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["mydatabase"]
        self.mycol = self.mydb["customers"]
        
    def insertPost(self, post:dict):
        post_id = self.mycol.insert_one(post).inserted_id
        print(post_id)
        
    def insertPosts(self, post:dict):
        post_id = self.mycol.insert_many(post).inserted_ids
        print(post_id)
        
    def getPost(self, query:dict):
        return self.mycol.find_one(query)
    
    def getPosts(self, query:dict):
        return self.mycol.find(query)
    
    def printPosts(self):
        for post in self.mycol.find():
            print.pprint(post)

    def returnPosts(self):
        for post in self.mycol.find():
            yield post

    def deletePost(self, query:dict):
        self.mycol.delete_one(query)
    
    #collection.delete_many(filter, collation=None, 
    # hint=None, session=None)
    
    def deleteAllPosts(self,query:dict):
        self.mycol.delete_many(query)
    
    


x = Database()
x.connect()

mydict = [
    { "name": "Dan", "address": "Taco 4251" },
    { "name": "Calvin", "address": "Taco 4251" },
    { "name": "Alvin", "address": "Taco 4251" },
    { "name": "Dalvin", "address": "Taco 4251" }
]
#x.insertPosts(mydict)
x.deleteAllPosts({})

# x.insertPosts(mydict)
