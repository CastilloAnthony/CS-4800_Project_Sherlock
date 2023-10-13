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
    
    def deletePosts(self,query:dict):
        self.mycol.delete_many(query)
        
# x = Database()
# x.connect()

class checkDatabase:
    def __init__(self):
        self.x = Database()
        self.x.connect()
    def check_insertPosts(self):
        mydict = [
            { "name": "Dan", "address": "Taco 4251" },
            { "name": "Calvin", "address": "Taco 4251" },
            { "name": "Alvin", "address": "Taco 4251" },
            { "name": "Dalvin", "address": "Taco 4251" }
        ]
        self.x.insertPosts(mydict)
    def check_deletePost(self):
        self.x.deletePosts({})
        print(x.getPost({"name":"Dan"}))
        print(x.getPost({"name":"Dan"})["name"])

    def input_dict(self):
        name = input("enter your name\nname : ")
        address = input("enter your address\naddress : ")
        
        self.x.insertPost({"name":name, "address":address})
        
x = checkDatabase()
x.check_insertPosts()