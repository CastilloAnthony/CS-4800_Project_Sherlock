# Created by Anthony Castillo
import pymongo
from time import ctime

class DBConnectionAgent():
    # Communicates directly with DB on behalf of the Server
    def __init__(self):
        """Initialization function setting client and db to false.
        """
        self.__client = False
        self.__db = False

    def __del__(self):
        """Deletion function that deletes the client and db variables.
        """
        self.disconnect()
        del self.__client
        del self.__db

    def connect(self, address="127.0.0.1", port="27017"):
        """Connects to a specified server

        Args:
            address (string): The IP Address of the server. Defaults to "localhost"
            port (string): The Port Number for the Server. Defaults to "27017"

        Returns:
            bool: Success/Failure to connect
        """
        try:
            self.__client = pymongo.MongoClient("mongodb://"+address+":"+port+"/")
            return True
        except:
            print("Could not connect to DB at: "+"mongodb://"+address+":"+port+"/")
            self.__client = False
            return False
        
    def disconnect(self):
        """Attempts to disconnect from the mongoDB.

        Returns:
            bool: True/False on success/failure.
        """
        if self.__client != False:
            self.__client.close()
            self.__client = False
            return True
        else:
            return False
        
    def createNewDB(self, name:str):
        """Attempts to creates a brand new mongoDB database named the inputted string.

        Args:
            name (str): The name of the database to be created.

        Returns:
            bool: True/False on success/failure.
        """
        if name not in self.getDBs():
            return self.__client[name]['Initial'].insert_one({'name':name, 'notes':'Created a new database named '+name, 'timestamp':ctime()}).acknowledged
        else:
            return False
    
    def getDBs(self):
        """Returns a List of databases for the connected system

        Returns:
            list: Returns a List of databases for the connected system in the format of ["admin", "config", "local"]
        """
        if self.__client != False:
            return self.__client.list_database_names()

    def useDB(self, db):
        """Sets the target DB

        Args:
            db (string): The DB to use, must be found inside of the getDBs() function

        Returns:
            bool: Success/Failure to use the specified DB
        """
        if db in self.getDBs():
            self.__db = self.__client[db]
            return True
        else:
            return False

    def addToDB(self, column:str, content:dict):
        """Adds data into the DB at the specified column

        Args:
            column (string): The column we wish to add data into
            content (dict): The content to add into the DB

        Returns:
            bool: Success/Failure to add content to the DB
        """
        if self.__db != False:
            self.__db[column].insert_one(content).acknowledged
            try:
                return self.__db[column].insert_one(content).acknowledged
            except:
                return False
        else:
            return False

    def removeFromDB(self, column:str, query:dict, remove:dict):
        #C.A.
        """Removes the first instance of an entry, within the column, that matches the inputted query.

        Args:
            column (str): The desired colleciton for which to remove data from.
            query (dict): The query used to match with data in the database.

        Returns:
            bool: True/False on success/failure.
        """
        # db.yourCollection.update_one(
        #     { _id: <ObjectId("your_document_id")> },
        #     { $pull: { 'websiteLists': "<removedWebsite>" } }
        # );
        if self.__db != False:
            return self.__db[column].update_one(
                query,
                {'$pull': remove}
            )
            #return self.__db[column].delete_one(query).acknowledged
        else:
            return False

    def removeManyFromDB(self, column:str, query:dict):
        """Removes all instances, from the column, that matches the inputted query.

        Args:
            column (str): The desired colleciton for which to remove data from.
            query (dict): The query used to match with data in the database.
        Returns:
            bool: True/False on success/failure.
        """
        if self.__db != False:
            return self.__db[column].delete_many(query).acknowledged
        else:
            return False

    def requestFromDB(self, column:str, query:dict):
        """Returns the first entry, from the column, that matches the inputted query.

        Args:
            column (str): The desired colleciton for which to request data from.
            query (dict): The query used to match with data in the database.

        Returns:
            bool: True/False on success/failure.
        """
        if self.__db != False:
            return self.__db[column].find_one(query)
        else:
            return False
    
    def requestManyFromDB(self, column:str, query:dict):
        """Takes in a request for a given collection and searches the database for content that matches the query.

        Args:
            column (str): The name of the collection that data is being requested from
            query (dict): _description_

        Returns:
            bool: False if a connection to the database has not yet been established
            list: A list of all the documents/dictionaries that 
        """
        if self.__db != False:
            tempData = []
            cur = self.__db[column].find(query)
            for doc in cur:
                tempData.append(doc)
            return tempData
        else:
            return False

    def clearDB(self, column:str):
        """Deletes everything from the database for the given collection/column

        Args:
            column (str): The name of the collection to be deleted

        Returns:
            bool: True/False for a successful/unsuccessful deletion of the contents of the collection
        """
        if self.__db != False:
            return self.__db[column].delete_many({}).acknowledged
        else:
            return False

    def verifyCollection(self, column:str):
        """Verifies that a collection/column exists within the database.

        Args:
            column (str): The name of the collection to be verified.

        Returns:
            bool: True/False for if the collection Exists or Does Not Exist
        """
        try:
            self.__db.validate_collection(column)
            return True
        except pymongo.errors.OperationFailure:
            return False

    def updateInDB(self, column:str, query:dict, changeTo:dict):
        #C.A.
        """Updates a single document in the database. 

        Args:
            column (str): The collection to modify
            query (dict): QUERY FORMAT EXAMPLE: query={'id':matchWithThis}, 
            quer (dict): changeTo={'id':ModifyToThis}

        Returns:
            bool: True/False for a successful/unsuccessful update
        """
        if self.__db != False:
            #update_one(<filter_criteria>, update_data)
            #filter_criteria = {"name": "John"}
            #update_data = {"$set": {"age": 30}}
            
            
            
            # print(query, '\n',changeTo)
            # query: {'_id': '6542ea812079dc2a9c74ca6d', 'name': 'adfa', 'presetLists': ['www.csustan.edu', 'www.bbc.co.uk', 'www.reddit.com', 'https://discord.gg/keAWQanBp8'], 'timestamp': 1698884225.4272666}
            # changeTo: {'_id':preset_to_be_changed['_id'],'name':'taco', 'presetLists':['www.google.com', 'chat.openai.com', 'www.bbc.co.uk'], 'timestamp':preset_to_be_changed['timestamp']}
            
            #changeTo: Needs to be in form:
            #{
            #     'presets': {
            #         'name': 'John',
            #         'presetLists': ['www.example1.com', 'www.example2.com'],
            #         'timestamp': 1698890950.1513646
            #     }
            # }
            return self.__db[column].update_one(
                query, 
                {"$push":
                    changeTo
                    }).acknowledged
            
            # return self.__db[column].update_one(query, {"$set":changeTo}).acknowledged
        else:
            return False
        
    def update2InDB(self, column:str, query:dict, old:dict, changeTo:dict):
        #c.a.
        if self.__db != False:
            #remove old preset
            self.__db[column].update_one(
                query,
                {'$pull': old}
            )
            #add new preset
            return self.__db[column].update_one(
                query, 
                {"$push":
                    changeTo
                    }).acknowledged
        else:
            return False
        
        # self.__db[column].update_one(filter_query, new_values, array_filters=[{'elem.name': 'existing_name', 'elem.email': 'existing_email'}])
        

#end DBConnecitonAgent
