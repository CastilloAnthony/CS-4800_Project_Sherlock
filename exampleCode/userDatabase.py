# use website: https://www.mongodb.com/try/download/community
# download mongodb version 7.0
import pymongo
class UserDatabase:
    def __init__(self):
        self.myclient = False
        self.mydb = False
        self.mycol = False
    
    def connect(self, collection:str):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["BirdWatchers_Test"]
        self.mycol = self.mydb[collection]
    
    def find_user_by_name(self, name):
        return self.mycol.find_one({"name": name})

    def find_user_by_email(self, email):
        return self.mycol.find_one({"email": email})

    def insert_user(self, user_data):
        self.mycol.insert_one(user_data)

    def update_user_password(self, email, new_password):
        self.mycol.update_one({"email": email}, {"$set": {"password": new_password}})
    
    
    
    def getPost(self, query:dict):
        return self.mycol.find_one(query)
    
    def getPosts(self, query:dict):
        return self.mycol.find(query)

    def returnPosts(self):
        for post in self.mycol.find():
            yield post

    def deletePost(self, query:dict):
        self.mycol.delete_one(query)
    
    #mycol.delete_many(filter, collation=None, 
    # hint=None, session=None)
    
    def deletePosts(self,query:dict):
        self.mycol.delete_many(query)
        
    def insertPost(self, post:dict):
        post_id = self.mycol.insert_one(post).inserted_id
        
    def insertPosts(self, post:dict):
        post_id = self.mycol.insert_many(post).inserted_ids
        
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